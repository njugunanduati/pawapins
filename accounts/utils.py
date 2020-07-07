import jwt
import time
import random
from django.conf import settings


def get_random():
    return random.randint(100000, 999999)


def reset_password_token(email, expires_in=600):
    return jwt.encode(
        {'reset_password': email, 'exp': time.time() + expires_in},
        settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
