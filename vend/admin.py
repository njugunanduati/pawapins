from django.contrib import admin

from .models import Token, Sms, Reversal, SmsSent


admin.site.register(Token)
admin.site.register(Sms)
admin.site.register(Reversal)
admin.site.register(SmsSent)



