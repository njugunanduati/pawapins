import json
import pytz

from datetime import datetime, timedelta, timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.generic.base import View
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

class SmsView(View):

	def post(self, request):
		date_recieved = request.POST['date']
		msisdn = request.POST['from']
		at_id = request.POST['id']
		link_id = request.POST['linkId']
		message = request.POST['text']
		to = request.POST['to']
		network_code = request.POST['networkCode']
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
		data['msisdn'] = msisdn
		data['message'] = message
		return HttpResponseRedirect(reverse('vend', args=(),
			kwargs={'msisdn' : msisdn, 'message' : message }))



class VendView(View):
	client = settings.CLIENT
	term = settings.TERMINAL
	ip = settings.IP
	port = settings.PORT
	buffer_size = settings.BUFFER_SIZE
	today = settings.date_today
	my_ref = get_rand()

	def get(self, request):
		msisdn = request.GET['msisdn']
		message = request.GET['message']
		data = message.split('#')
		pin = data[0]
		meter = data[1]
		card = Card.objects.filter(pin=pin, status=0).get()
		amount = card.batch.denomination
		ipay_connect = IpayConnect(self.ip, self.port, self.client, self.term, meter, amount, self.today, self.my_ref)
		vend = ipay_connect.make_vend()
		if vend['code'] == "elec000":
			card = Card.objects.filter(pin=pin).get()
			card.status = 1
			used_by = msisdn
			active=False
			card.save()
			# save the vend data
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
				meter=meter,
				amount_paid=amount,
				pin=pin
			)
			token.save()
			# send sms
			message = 'Meter: {}, Token: {}, Amount: {}'.format(meter, vend['token'], amount)
			return HttpResponse(send_sms(message, msisdn))
		elif vend['code'] == "elec003":
			pass
		elif vend['code'] == "elec004":
			pass
		else:
			pass
