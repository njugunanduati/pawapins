from core.utils import send_email
from django.urls import reverse

from core.utils import build_absolute_url
from django.conf import settings


__all__ = (
    "send_forgot_password_request",
    "send_change_password",
    "send_login_token"
)


def send_forgot_password_request(user, reset_password_token):
    reset_password_path = reverse(
        "accounts:reset_password",
        kwargs=dict(reset_token=str(reset_password_token)),
    )
    print("+++",  build_absolute_url(reset_password_path))

    subject = "Reset your {site_name} password".format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name="emails/forgot_password_request.html",
        context={
            "reset_password_url": build_absolute_url(reset_password_path),
        },
        to=[user.email],
    )


def send_change_password(user):

    subject = "Your {site_name} password has been changed successfully".format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name="emails/change_password.html",
        context={},
        to=[user.email],
    )


def send_login_token(user, token):

    subject = "{site_name} login token".format(
        site_name=settings.SITE_NAME
    )

    send_email(
        subject=subject,
        template_name="emails/login_token.html",
        context={'token': token},
        to=[user.email],
    )
