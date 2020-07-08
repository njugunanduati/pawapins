from django.dispatch import Signal

new_sms_received = Signal(providing_args=["pin", "meter", 'msisdn'])
