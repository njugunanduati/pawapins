from django.urls import path, include

from .views import (
    VendView, SmsView, SmsRecievedView, SmsSentView, TokenView
)

app_name = "vend"
urlpatterns = [
    path("vend/", VendView.as_view(), name="vend"),
    path("sms/", SmsView.as_view(), name="sms"),
    path("sms_recieved", SmsRecievedView.as_view(), name="sms_recieved"),
    path("sms_sent", SmsSentView.as_view(), name="sms_sent"),
    path("tokens", TokenView.as_view(), name="tokens"),
]
