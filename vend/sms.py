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
        return 'The sms error : {}'.format(str(e))


# {
#     'statusCode': 101, 
#     'number': '+254729556997', 
#     'cost': 'KES 0.8000',
#     'status': 'Success', 
#     'messageId': 'ATXid_c2f1aec156b318ff999de775d38bfbb9'
# }