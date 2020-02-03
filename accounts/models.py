import uuid
import string
import random

from datetime import datetime
from hashlib import md5
from time import time
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from django.conf import settings


class Profile(TimeStampedModel):
    phone_number = models.CharField(max_length=14, null=True)
    reset_password_token = models.CharField(
        max_length=300, editable=False, null=True)
    reset_password_request_date = models.DateTimeField(null=True)
    login_token = models.CharField(
        max_length=300, editable=False, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __repr__(self):
        return self.user.username

    def get_login_token(self):
        return self.login_token

    def generate_password_request_date(self):
        self.reset_password_request_date = timezone.now()
