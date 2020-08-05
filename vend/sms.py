#!/usr/bin/python3
import requests
import africastalking
from lxml import etree
from config import settings
from .models import SmsSent


# def send_sms(message, msisdn):
# 	username = settings.AT_USERNAME
# 	api_key = settings.AT_API_KEY
# 	data = {}
# 	try:
# 		africastalking.initialize(username, api_key)
# 		sms = africastalking.SMS
# 		response = sms.send(message, [msisdn])
# 		sms_data = response['SMSMessageData']
# 		data['message'] = sms_data['Message']
# 		data['phone_number'] = msisdn
# 		for r in sms_data['Recipients']:
# 			data['message_id'] = r['messageId']
# 			data['cost'] = r['cost']
# 			data['status'] = r['status']
# 			data['status_code'] = r['statusCode']
#
# 		sms_sent = SmsSent(
# 			msisdn=data['phone_number'],
# 			message=data['message'],
# 			sent_text=message,
# 			cost=data['cost'],
# 			status=data['status'],
# 			message_id=data['message_id']
# 		)
# 		sms_sent.save()
# 		print('msg', response)
# 		return response
# 	except Exception as e:
# 		return 'There is an sms error! {}'.format(str(e))


def send_sms(message, msisdn):
    url = settings.SMS_URL
    host = settings.SMS_HOST
    sms_sender_id = settings.SMS_SENDER_ID
    sms_app_name = settings.SMS_APP_NAME
    sms_username = settings.SMS_USERNAME
    sms_password = settings.SMS_PASSWORD
    sms_priority_int = settings.SMS_PRIORITY

    headers = {
        "Host": host,
        "Content-Type": "text/xml; charset=utf-8",
        "SOAPAction": "http://tempuri.org/SendSMSWithPriority"
    }
    soap_ns = 'http://schemas.xmlsoap.org/soap/envelope/'
    ns_map = {'soap': soap_ns}
    envelope = etree.Element(etree.QName(soap_ns, 'Envelope'), nsmap=ns_map)
    body = etree.SubElement(envelope, etree.QName(soap_ns, 'Body'), nsmap=ns_map)
    sms_priority = etree.SubElement(body, 'SendSMSWithPriority', xmlns="http://tempuri.org/")
    recipient = etree.SubElement(sms_priority, 'Recipient')
    recipient.text = str(msisdn)
    text = etree.SubElement(sms_priority, 'Text')
    text.text = str(message)
    app_name = etree.SubElement(sms_priority, 'AppName')
    app_name.text = str(sms_app_name)
    sender_id = etree.SubElement(sms_priority, 'SenderID')
    sender_id.text = str(sms_sender_id)
    reference = etree.SubElement(sms_priority, 'Reference')
    reference.text = 'mytest'
    username = etree.SubElement(sms_priority, 'UserName')
    username.text = str(sms_username)
    password = etree.SubElement(sms_priority, 'Password')
    password.text = str(sms_password)
    priority = etree.SubElement(sms_priority, 'Priority')
    priority.text = str(sms_priority_int)
    params = etree.tostring(envelope, pretty_print=True, encoding='utf-8')
    try:
        response = requests.post(url, data=params, headers=headers)
        sms_sent = SmsSent(
            msisdn=msisdn,
            message=message,
            sent_text=message
        )
        sms_sent.save()
        print('msg', response.text)
        return response
    except Exception as e:
        return 'There is an sms error! {}'.format(str(e))
