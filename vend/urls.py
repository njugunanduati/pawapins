from django.urls import path, include

from .views import (
    VendView, SmsView,
)

app_name = "vend"
urlpatterns = [
    path("vend/", VendView.as_view(), name="vend"),
    path("sms/", SmsView.as_view(), name="sms"),
]
