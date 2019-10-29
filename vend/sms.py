#!/usr/bin/python3
import africastalking
from config import settings

# Initialize SDK
username = settings.AT_USERNAME
api_key = settings.AT_API_KEY
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# Use the service synchronously
def send_sms(message, msidn):
	response = sms.send(message, [msidn])
	return response