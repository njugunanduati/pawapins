import json
import pytz

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
from .utils import get_rand

from .models import Token, Reversal, Sms, SmsSent
from pins.models import Subscriber, Card
from .sms import send_sms


class SmsRecievedView(LoginRequiredMixin, TemplateView):
    template_name = "sms.html"
    title = 'Sms Recieved'

    def get_context_data(self, **kwargs):
        context = super(SmsRecievedView, self).get_context_data(**kwargs)
        context["sms"] = Sms.objects.all()
        context["title"] = self.title
        return context


class SmsSentView(LoginRequiredMixin, TemplateView):
    template_name = "sms_sent.html"
    title = 'Sms Sent'

    def get_context_data(self, **kwargs):
        context = super(SmsSentView, self).get_context_data(**kwargs)
        context["sms"] = SmsSent.objects.all()
        context["title"] = self.title
        return context


class TokenView(LoginRequiredMixin, TemplateView):
    template_name = "tokens.html"
    title = 'Tokens'

    def get_context_data(self, **kwargs):
        context = super(TokenView, self).get_context_data(**kwargs)
        context["tokens"] = Token.objects.all()
        context["title"] = self.title
        return context

@method_decorator(csrf_exempt, name='dispatch')
class SmsView(View):
	client = settings.CLIENT
	term = settings.TERMINAL
	ip = settings.IP
	port = settings.PORT
	buffer_size = settings.BUFFER_SIZE
	today = settings.date_today
	my_ref = get_rand()

	def post(self, request, *args, **kwargs):
		data = request.POST
		print("data", data)
		date_recieved = data['date']
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
			date_recieved=date_recieved,
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
			card = Card.objects.filter(pin=pin, status=0).get()
		except ObjectDoesNotExist:
			return JsonResponse({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
		amount = card.batch.denomination
		ipay_connect = IpayConnect(
			self.ip, self.port, self.client, self.term, meter, amount, self.today, self.my_ref)
		vend = ipay_connect.make_vend()
		card.status = 1
		card.used_by = msisdn
		card.active=False

		try:
			card.save()
		except Exception as e:
			content = "Error updating pin details"
			return HttpResponse(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		card.save()
		# save the vend data
		print("vend", vend)

		token = Token(
			vend_time=vend['vend_time'],
			reference=vend['reference'],
			address=vend['address'],
			code=vend['code'],
			token=vend['token'],
			units=round(vend['units'], 2),
			units_type=vend['units_type'],
			amount=vend['amount'],
			tax=vend['tax'],
			tarrif=vend['tarrif'],
			description=vend['description'],
			rct_num=vend['rct_num'],
			phone_number=msisdn,
			meter=meter,
			amount_paid=amount,
			pin=pin
		)


		try:
			token.save()
		except Exception as e:
			content = "Error generating the token"
			return HttpResponse(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		# send sms
		message = 'Meter: {}, Token: {}, Amount: Ksh {}, Units: {}'.format(meter, vend['token'], amount, token.units)
		msg = send_sms(message, msisdn)
		print("msg", msg)
		content = "The token has been sent to the user"
		return HttpResponse(content, status=status.HTTP_200_OK)
