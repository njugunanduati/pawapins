import jwt
import time
from django.conf import settings

def reset_password_token(email, expires_in=600):
    return jwt.encode(
        {'reset_password': email, 'exp': time.time() + expires_in},
        settings.SECRET_KEY, algorithm='HS256').decode('utf-8')