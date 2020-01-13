import json
import pytz
import time

from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .ipay import IpayConnect
from config import settings
from .utils import get_rand, get_sec_normal

from .models import Token, Reversal, Sms, SmsSent
from pins.models import Subscriber, Card
from .sms import send_sms


class SmsRecievedView(LoginRequiredMixin, TemplateView):
    template_name = "sms.html"
    title = 'Sms Recieved'

    def get_context_data(self, **kwargs):
        context = super(SmsRecievedView, self).get_context_data(**kwargs)
        context["sms"] = Sms.objects.all().order_by('-created')
        context["title"] = self.title
        return context


class SmsSentView(LoginRequiredMixin, TemplateView):
    template_name = "sms_sent.html"
    title = 'Sms Sent'

    def get_context_data(self, **kwargs):
        context = super(SmsSentView, self).get_context_data(**kwargs)
        context["sms"] = SmsSent.objects.all().order_by('-created')
        context["title"] = self.title
        return context


class TokenView(LoginRequiredMixin, TemplateView):
    template_name = "tokens.html"
    title = 'Tokens'

    def get_context_data(self, **kwargs):
        context = super(TokenView, self).get_context_data(**kwargs)
        context["tokens"] = Token.objects.all().order_by('-created')
        context["title"] = self.title
        return context


@csrf_exempt
def sms_post(request):
    client = settings.CLIENT
    term = settings.TERMINAL
    ip = settings.IP
    port = settings.PORT
    buffer_size = settings.BUFFER_SIZE
    today = settings.date_today
    my_ref = get_rand()
    rev_ref = get_rand()
    app_cert = settings.APP_CERT
    app_key = settings.APP_KEY
    seq = get_sec_normal()

    data = request.POST
    print("data", data)
    date_received = data['date']
    msisdn = data['from']
    at_id = data['id']
    if data['linkId']:
        link_id = data['linkId']
    else:
        link_id = 0
    message = data['text']
    to = data['to']
    network_code = data['networkCode']
    sms = Sms(
        date_recieved=date_received,
        msisdn=msisdn,
        at_id=at_id,
        link_id=link_id,
        message=message,
        to=to,
        network_code=network_code
        )
    sms.save()
    data = {}
    data['msisdn'] = msisdn
    data['message'] = message
    msisdn = data['msisdn']
    message = data['message']
    data = message.split('#')
    pin = data[0].split(' ')
    pin = pin[1]
    meter = data[1]
    try:
        card = Card.objects.filter(pin=pin).get()
    except ObjectDoesNotExist:
        message = 'Pin does not exist'
        msg = send_sms(message, msisdn)
        print("msg", msg)
        return HttpResponse(message, status=status.HTTP_200_OK)
    if card.status != 0:
        message = 'Pin has already been used'
        msg = send_sms(message, msisdn)
        print("msg", msg)
        return HttpResponse(message, status=status.HTTP_200_OK)

    amount = card.batch.denomination
    ipay_connect = IpayConnect(
        ip, port, client, term, meter, amount, today, my_ref, rev_ref, app_cert, app_key, seq)

    vend = ipay_connect.make_vend()

    # save the vend data
    print("vend", vend)

    if vend['code'] is 'elec001':
        message = 'Incorrect meter number'
        msg = send_sms(message, msisdn)
        return HttpResponse(message, status=status.HTTP_200_OK)
    elif 'vend_rev_time' in vend:
        message = 'Technical issue please try after some time'
        card.save()
        msg = send_sms(message, msisdn)
        return HttpResponse(message, status=status.HTTP_200_OK)
    elif vend['code'] == 'elec003':
        message = 'No record found'
        card.save()
        msg = send_sms(message, msisdn)
        return HttpResponse(message, status=status.HTTP_200_OK)

    # update card details
    card.status = 1
    card.used_by = msisdn
    card.active=False
    card.save()

    token = Token(
        vend_time=vend['vend_time'],
        reference=vend['reference'],
        address=vend['address'],
        code=vend['code'],
        token=vend['token'],
        units=vend['units'],
        units_type=vend['units_type'],
        amount=vend['amount'],
        tax=vend['tax'],
        tarrif=vend['tarrif'],
        description=vend['description'],
        rct_num=vend['rct_num'],
        phone_number=msisdn,
        meter=meter,
        amount_paid=amount,
        pin=pin,
        seq=seq
    )

    try:
        token.save()
    except Exception as e:
        message = "Error generating the token"
        print("msg", message)
        return HttpResponse(message, status=status.HTTP_200_OK)
    # send sms
    message = 'Meter: {}, Token: {}, Amount: Ksh {}, Units: {}'.format(meter, vend['token'], amount, token.units)
    msg = send_sms(message, msisdn)
    message = "The token has been sent to the user"
    return HttpResponse(message, status=status.HTTP_200_OK)
