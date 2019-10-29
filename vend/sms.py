#!/usr/bin/python3
import africastalking
from config import settings


def send_sms(message, msidn):
    username = settings.AT_USERNAME
    api_key = settings.AT_API_KEY
    try:
        africastalking.initialize(username, api_key)
        sms = africastalking.SMS
        return sms.send(message, [msidn])
    except Exception as e:
        raise 'The sms error : {}'.format(str(e))