import os

from . import local_settings
import re
from django.contrib.admin import sites

#set your own enviroment for what you want
#ENVIRONMENT = os.getenv('ENVIRONMENT', 'developmentLocalNate', 'developmentLocalNick', 'devlomentLiveHeroku')

ENVIRONMENT = local_settings.ENVIRONMENT
DEBUG = local_settings.DEBUG

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = [
    '.localhost',
    'localhost', 'vendor.localhost',
    '10.0.0.53', 'vendor.10.0.0.53',
    'simntxdev.herokuapp.com', 'vendor.simntxdev.herokuapp.com',
    'simntx.herokuapp.com', 'vendor.simntx.herokuapp.com',
    '127.0.0.1', 'vendor.127.0.0.1',
]

# must make migrations and migrate after adding apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Auth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'django_countries',
    'stripe',

    # Custom
    'core',
    'dashboards',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simntx.middleware.auth_req.AuthRequiredMiddleware'
]

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
            'builtins': [
                'core.templatetags.tags',
            ]
        },
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_in_env')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if ENVIRONMENT == 'developmentLocalNick':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, 'db.sqlite3')
        }
    }

if ENVIRONMENT == 'developmentLocalNate':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "psql",
            "USER": "nfishel",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "5432",
            }
    }

if ENVIRONMENT == 'developmentLiveHeroku':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "dai1klnpvfaja0",
            "USER": "cgovsgkihvelvu",
            "PASSWORD": "991cb9de5f5b9ca3a4d0dbf51d48a17862735567d0994a3441161ea7898c0e6f",
            "HOST": "ec2-52-72-65-76.compute-1.amazonaws.com",
            "PORT": "5432",
            }
    }


if ENVIRONMENT == 'production':
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_REDIRECT_EXEMPT = []
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# AUTH
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
# CRISPY FORMS

LOGIN_EXEMPT_URLS = (
    r'^account/login/$',
    r'^account/logout/$',
    r'^account/signup/$',
     r'^landing/$',

)

CRISPY_TEMPLATE_PACK = 'bootstrap4'

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 10
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5

ACCOUNT_FORMS = {'signup': 'core.forms.UserSignUpForm'}

ROOT_URLCONF = 'simntx.urls'

# STRIPE SETTINGS
# if DEBUG:
STRIPE_PUBLIC_KEY = 'pk_test_51GtkimASycExiKjqwnRJpXJt8fySzvcRbeu14D7Ojazha64RDUuID9kVhCfeHlfOCFOJbKbZ9pOMFvVKelhY8jrV009FTiquzO'
STRIPE_SECRET_KEY = 'sk_test_51GtkimASycExiKjqfWXiucyq8NjoCsBWmTUNxbRyp3zmK0PJQckKKLfF22dahOlFzbzqi0NfQsBXatHWyui2lEWG00j2W27877'
# else:


EMAIL_HOST= 'smtp.gmail.com'
EMAIL_HOST_USER= 'simntxdev@gmail.com'
EMAIL_HOST_PASSWORD= 'omtEEWXmh23a'
EMAIL_USE_TLS= True
EMAIL_PORT= 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
