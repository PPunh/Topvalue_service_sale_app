"""
Django settings for apps project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os, sys
from pathlib import Path
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-04p-1al#avxqx*snktubg%hihlx-8$fhm#e@h%+8oznn(t09nt'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application defination
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.humanize',

    # 3rd party apps
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'django_filters',
    'widget_tweaks',
    #'django_ratelimit', # rate limit, uncomment this line in production deployment
    'axes', # tracking user login fail attempts

    # custom apps
    # usage: apps.app_name
    'apps.users', # custom users app, extending the default built-in Django Auth
    'apps.app_customers',
    'apps.app_employies',
    'apps.app_quotations',
    'apps.app_invoices',
]

AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = [
    'apps.users.backends.MultiAuthBackend',  # custom authentication backend to allow login by email or phone number
    'axes.backends.AxesStandaloneBackend', # login fails limit
    'django.contrib.auth.backends.ModelBackend',  # Default ModelBackend as fallback
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 3rd party libs
    'whitenoise.middleware.WhiteNoiseMiddleware', # serving static file via django
    'axes.middleware.AxesMiddleware', # tracking user login fail attempts

    # custom libs
    'middleware.CustomRateLimitMeaage', # display custom text when a user or an IP is blocked
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('POSTGRES_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'PORT': '5432',
        'OPTIONS': {
            # tell django to use additional schema
            #'options': '-c search_path=public,fees',
        }
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'sqlite', 'db.sqlite3'),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# when DEBUG = True, disable cache during development
# when DEBUG = False, use memcached as cache in production
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
            'LOCATION': [
                'memcached:11211', # memcached = docker service name, use this if you use the included docker files
                #'127.0.0.1:11211', # use this if you don't use the included docker files
            ]
        }
    }


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

# j: Day of the month without leading zeros (1 to 31)
# N: Month abbreviation, in English, "Jan", "Feb", "Mar"
# Y: Four-digit year, e.g. "2024"
DATE_FORMAT = 'j N Y'

# tell Django to aware of timezone
USE_TZ = True

# set timezone to UTC +7, change tou your prefer timezone as need
TIME_ZONE = 'Asia/Vientiane'

# Django's internationalization (i18n) framework for multilingual development
USE_I18N = True

# Django's localization (l10n) framework.
# if user's locale is set to "en-US," a date might be displayed as "12/25/2023."
# if user's locale is set to "en-GB," a date might be displayed as "25/12/2023."
# works in conjunction with USE_I18N
USE_L10N = True

DEFAULT_CHARSET = 'utf-8'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# use WhiteNoise storage backend to server static files with compression
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    # Global static diretory
    os.path.join(BASE_DIR, 'templates', 'static'),

    # app specific static directory
    # each new app need to register its static dir here
    os.path.join(BASE_DIR, 'apps', 'users', 'templates', 'static'),
]

# base URL for media files uploaded by users
MEDIA_URL = '/media/'

# folder to store media file uploaded by users
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# URL to redirect after login if the contrib.auth.views.login view gets no "next" parameter
LOGIN_REDIRECT_URL = reverse_lazy('users:home')

# URL to redirect the user to login page if that pare require user login to access
LOGIN_URL = reverse_lazy('users:login')

# URL to redirect the user to after logout
LOGOUT_URL = reverse_lazy('users:login')

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

SPECTACULAR_SETTING = {
    'TITLE': 'API',
    'DESCRIPTION': 'API',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Make sessions expire when the browser is closed
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# (Optional) Set the session expiration time (e.g., 30 minutes of inactivity)
SESSION_COOKIE_AGE = 10800  # 3 hrs (in seconds)

# django core email backend for development use, it sends email to console
# so during development we don't need to setup real email system to see sample
# email messages
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# This setting use external email server to send email, to use it,
# disable the 'django.core.mail.backends.console.EmailBackend' above
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'xxx@gmail.com'
# EMAIL_HOST_PASSWORD = 'xxx'

# Axes, tracking login fails, settings
AXES_FAILURE_LIMIT = 50  # Number of login failed attempts before blocking
AXES_ONLY_USER_PER_IP = True # If True, it will block the IP address instead of the user.
AXES_LOCKOUT_MINUTES = 60  # Block duration in minutes
AXES_IP_LOCKOUT_MINUTES = 60 # Block duration for IP addresses
AXES_COOLOFF_TIME = 300 # in seconds after a successful login, this helps prevent brute-force attacks
# immediately after a successful login.
AXES_ADMIN_INTERFACE_ENABLED = True # enable the Django admin interface for managing blocked users/IPs.

# Django-ratelimit setting
# Use case: set to False when you are using other DDOS protection such as Web Application Firewall or cloudflare
RATELIMIT_ENABLE = True
RATE_LIMIT = '1000/5m' # 1000 requests within 5 minutes from single IP
