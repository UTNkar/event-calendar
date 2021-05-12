from .base import *
from decouple import config

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('DJANGO_SECRET')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DJANGO_DB_NAME', default='event_calendar'),
        'USER': config('DJANGO_DB_USER', default='event_calendar'),
        'PASSWORD': config('DJANGO_DB_PASS', default=''),
        'HOST': config('DJANGO_DB_HOST', default='127.0.0.1'),
        'PORT': config('DJANGO_DB_PORT', default='5432'),
    }
}

ALLOWED_HOSTS = ['.utn.se']

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_DOMAIN = '.utn.se'

SESSION_COOKIE_SECURE = True
