# -*- coding: utf-8 -*-
from .base import *


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
        'CONN_MAX_AGE': 600,
    }
}

# Email Reporting
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_PORT = 465
SERVER_EMAIL = config('SERVER_EMAIL')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True

# Sessions and Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# session expiration
SESSION_EXPIRE_SECONDS = 300
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True

# Enable HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF=True
