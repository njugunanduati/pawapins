import os
from unipath import Path
import environ
import pytz

from datetime import datetime, timedelta, timezone

# date 
date_today = datetime.now(pytz.timezone('Africa/Nairobi')).strftime("%Y-%m-%d %H:%M:%S %z")

# read variables for .env file
ENV = environ.Env()
environ.Env.read_env(".env")

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tn^6$ry6$=^e2um&izfj(a5hy83o+hs^ab9g#n(-(x$5p=7*pa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '173.230.137.108', 
    '127.0.0.1',
    'localhost',
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_adminlte',
    'accounts',
    'core',
    'pins',
    'vend',
    'crispy_forms',
]

# crispy template pack
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ENV.str("DB_NAME", ""),
        'USER': ENV.str("DB_USER", ""),
        'PASSWORD': ENV.str("DB_PASSWORD", ""),
        'HOST': ENV.str("DB_HOST", ""),
        'PORT': ENV.str("DB_PORT", ""),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


EMAIL_HOST = ENV.str("EMAIL_HOST")
EMAIL_PORT = ENV.int("EMAIL_PORT", )
EMAIL_HOST_USER = ENV.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = ENV.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = ENV.bool("EMAIL_USE_TLS", True)


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'


SITE_NAME = "PawaPins"
BASE_URL = ENV.str("BASE_URL", "")
LOGIN_REDIRECT_URL = "/accounts/dashboard/"


# bizswitch credentials
CLIENT = ENV.str("CLIENT", "")
TERMINAL = ENV.str("TERMINAL", "")
IP=ENV.str("IP", "")
PORT=ENV.str("PORT", "")
BUFFER_SIZE=ENV.str("BUFFER_SIZE", "")

# africastalking credentials
AT_USERNAME = ENV.str("AT_USERNAME", "")
AT_API_KEY = ENV.str("AT_API_KEY", "")
