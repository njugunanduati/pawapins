from django.urls import path, include

from .views import sms_post, SmsRecievedView, SmsSentView, TokenView

app_name = "vend"
urlpatterns = [
    path("sms/", sms_post, name="sms"),
    path("sms_received", SmsRecievedView.as_view(), name="sms_received"),
    path("sms_sent", SmsSentView.as_view(), name="sms_sent"),
    path("tokens", TokenView.as_view(), name="tokens"),
]
