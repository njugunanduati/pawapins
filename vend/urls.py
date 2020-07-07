from django.urls import path, include

from .views import (
    sms_post, check_sms, SmsReceivedView, SmsSentView, TokenView, check_test_sms
)

app_name = "vend"
urlpatterns = [
    path("sms/", sms_post, name="sms"),
    path("check_sms/", check_test_sms, name="check_sms"),
    path("sms_received", SmsReceivedView.as_view(), name="sms_received"),
    path("sms_sent", SmsSentView.as_view(), name="sms_sent"),
    path("tokens", TokenView.as_view(), name="tokens"),
]
