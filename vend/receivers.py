from django.dispatch import receiver
from vend.models import Sms
from .signals import *
from .views import buy_token


@receiver(new_sms_received)
def save_new_sms(sender, **kwargs):
    meter = kwargs['meter']
    pin = kwargs['pin']
    msisdn = kwargs['msisdn']
    return buy_token(sms=sender, meter=meter, pin=pin, msisdn=msisdn)
