import os

from . import local_settings
import re
from django.contrib.admin import sites

#set your own enviroment for what you want
#ENVIRONMENT = os.getenv('ENVIRONMENT', 'developmentLocalNate', 'developmentLocalNick', 'devlomentLiveHeroku')

ENVIRONMENT = local_settings.ENVIRONMENT
DEBUG = True
USE_S3 = True

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '-05sgp9!deq=q1nltm@^^2cc+v29i(tyybv3v2t77qi66czazj'
ALLOWED_HOSTS = [
    '.localhost',
    'localhost', 'vendor.localhost',
    '10.0.0.53', 'vendor.10.0.0.53',
    'simntxdev.herokuapp.com', 'vendor.simntxdev.herokuapp.com',
    'simntx.herokuapp.com', 'vendor.simntx.herokuapp.com', 'simntx-live.herokuapp.com',
    '127.0.0.1', 'vendor.127.0.0.1', 'http://www.simntx.net/', 'www.simntx.net','www.simntx.com'
]

# must make migrations and migrate after adding apps
INSTALLED_APPS = [
    #'whitenoise.runserver_nostatic',
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

    #S3 storage
    'storages',

    # Custom
    'core',
    'dashboards',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'simntx.middleware.auth_req.AuthRequiredMiddleware'
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

USE_S3 = os.getenv('USE_S3') == 'TRUE'

if USE_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AKIATOTJI2BKFIJUCHYI')
    AWS_SECRET_ACCESS_KEY = os.getenv('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')
    AWS_STORAGE_BUCKET_NAME = os.getenv('django-static-simntx')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    AWS_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')


if (DEBUG == False):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "d3v4ll78418ovf",
            "USER": "tdwtocjocvuysq",
            "PASSWORD": "df50fc64a2ab062534f1e5f212eb3de7c53e133dc550d509f27b56f2cec71c86",
            "HOST": "ec2-50-19-26-235.compute-1.amazonaws.com",
            "PORT": "5432",
            }
    }
else:
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
  
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'


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
    r'^store',
    r'^account/login/$',
    r'^accounts/login/$',
    r'^account/logout/$',
    r'^accounts/signup/$',
    r'^accounts/confirm-email/[a-zA-Z0-9]/$',
    r'^landing/$',
    r'^admin'
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
# if DEBUG == True:
STRIPE_PUBLIC_KEY = 'pk_live_51H6HtIBIRW4ci3BhZLMNo2GrB2F79zFZtwF0OgmHH42tWNvlCOoNv4WSMebIVsEfDJ5Y7XxKQb4ddsxjQLceC1LV00GsItcgxk'
STRIPE_SECRET_KEY = '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'
# else:
# STRIPE_PUBLIC_KEY = 'pk_test_51H6HtIBIRW4ci3Bhs3n98Lmeb9sZiXLnKpKsWVxp3BU0ULH4rnv8KtPl6MgA8WzBia6Muc7ZE1E84MSHiR9HrwrJ00WpXuvaSn'
# STRIPE_SECRET_KEY = 'sk_test_51H6HtIBIRW4ci3Bh2WYF9bkxfJZydcTVgosqEVhzlsrDS2fhgmMFd3bCo6Rn7bFgx6TtOZLYKgX8zI1ltidHvja600x1w3CRGz'

EMAIL_HOST= 'smtp.gmail.com'
EMAIL_HOST_USER= 'simntxdev@gmail.com'
EMAIL_HOST_PASSWORD= 'omtEEWXmh23a'
EMAIL_USE_TLS= True
EMAIL_PORT= 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'