#!/usr/bin/python3
import africastalking
from config import settings
from .models import SmsSent


def send_sms(message, msisdn):
	username = settings.AT_USERNAME
	api_key = settings.AT_API_KEY
	data = {}
	try:
		africastalking.initialize(username, api_key)
		sms = africastalking.SMS
		response = sms.send(message, [msisdn])
		sms_data = response['SMSMessageData']
		data['message'] = sms_data['Message']
		data['phone_number'] = msisdn
		for r in sms_data['Recipients']:
			data['message_id'] = r['messageId']
			data['cost'] = r['cost']
			data['status'] = r['status']
			data['status_code'] = r['statusCode']

		sms_sent = SmsSent(
			msisdn=data['phone_number'],
			message=data['message'],
			sent_text=message,
			cost=data['cost'],
			status=data['status'],
			message_id=data['message_id']
		)
		sms_sent.save()
		print('msg', response)
		return response
	except Exception as e:
		return 'There is an sms error! {}'.format(str(e))