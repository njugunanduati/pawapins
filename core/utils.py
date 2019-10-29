from typing import List, Tuple, Union

from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMessage


__all__ = (
    "send_email",
    "build_absolute_url",
)

def send_email(subject, template_name, context, to):
    if not to:
        return
    body = render_to_string(template_name)
    email = EmailMessage(
        subject=subject,
        body=body,
        to=to)
    # Setting the main content
    email.content_subtype = "html"
    email.send()


def build_absolute_url(path):
    return "{base_url}{path}".format(
        base_url=settings.BASE_URL,
        path=str(path),
    )
