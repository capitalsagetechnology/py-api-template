import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
import sentry_sdk
from decouple import config
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = int(os.environ.get("DEBUG", 1))
APP_DESCRIPTION = os.environ.get('APP_DESCRIPTION', 'App Name')

ALLOWED_HOSTS = ["127.0.0.1", "0.0.0.0", "localhost", "api",]
INTERNAL_IPS = ["127.0.0.1"]
if DEBUG:
    import os  # only if you haven't already imported this
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + '1' for ip in ips] + ['127.0.0.1', '10.0.2.2']

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'storages',
    'rest_framework',
    'django_filters',
    'import_export',
    'debug_toolbar',
    'drf_spectacular',
    'django_extensions',
    'core.celery.CeleryConfig',
    'user.apps.UserConfig',
]

AUTH_USER_MODEL = "user.User"

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ValidationErrorMiddleware',
    'core.middleware.CaptureExceptionMiddleware',
]

ROOT_URLCONF = 'core.urls'
IMPORT_EXPORT_USE_TRANSACTIONS = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = ['https://*.cintrustmfb.com', 'http://localhost:30001']
LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

JAZZMIN_SETTINGS = {
    "site_title": APP_DESCRIPTION,
    "site_header": APP_DESCRIPTION,
}

# Database

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

DATE_INPUT_FORMATS = [
    '%d/%m/%Y', '%d/%m/%y',  # '10/02/2020', '10/02/20'
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',  # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',  # 'October 25, 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October 2006'
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomPagination',
    'PAGE_SIZE': 12,
    # 'DATE_INPUT_FORMATS': ["%d/%m/%Y", ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STORAGE = os.getenv('STORAGE')

APP_NAME = os.getenv('APP_NAME')
# STATIC_LOCATION = f'{APP_NAME}/static'
# MEDIA_LOCATION = f'{APP_NAME}/media'

if STORAGE == 'S3':
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('ACCESS_SECRET')
    AWS_STORAGE_BUCKET_NAME = os.getenv('BUCKET_NAME')
    AWS_REGION_NAME = os.getenv('REGION_NAME')
    AWS_S3_ENDPOINT_URL = f'https://{AWS_REGION_NAME}.digitaloceanspaces.com'
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
    AWS_LOCATION = f'{APP_NAME}/static'
    STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # public media settings
    PUBLIC_MEDIA_LOCATION = f'{APP_NAME}/media'
    MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'core.storage_backends.PublicMediaStorage'
    # private media settings
    # PRIVATE_MEDIA_LOCATION = f'{APP_NAME}/private'
    # PRIVATE_FILE_STORAGE = 'core.storage_backends.PrivateMediaStorage'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'

# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    'handlers': {
        'logtail': {
            'class': 'logtail.LogtailHandler',
            'source_token': os.getenv('LOGTAIL_SOURCE_TOKEN'),
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    'loggers': {
        "": {
            "handlers": [
                "logtail",
            ],
            "level": "INFO",
        },
        'django': {
            'handlers': ['console', 'logtail'],
            'level': 'INFO',
            'propagate': True,
        },
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    }
}

# Email Settings
EMAIL_FROM = os.environ.get('SENDER_EMAIL')
EMAIL_HOST = os.environ.get('SMTP_HOST')
EMAIL_HOST_USER = os.environ.get('SMTP_USER')
EMAIL_HOST_PASSWORD = os.environ.get('SMTP_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

CLIENT_URL = os.environ.get('CLIENT_URL')
TOKEN_LIFESPAN = 24 * 7  # hours

REDIS_URL = os.getenv('REDIS_URL', 'localhost:6379')

CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

FLOWER_BASIC_AUTH = os.environ.get('FLOWER_BASIC_AUTH')
# Assumes that the username is swift or simple have the url as redis://swift:jetSwift@localhost:6379/0
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": APP_NAME
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHE_TTL = 60 * 1
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [REDIS_URL],
        },
        # 'ROUTING': 'core'
    },
}

CELERY_BEAT_SCHEDULE = {
    # "sample_task": {
    #     "task": "user.tasks.sample_task",
    #     "schedule": crontab(minute="*/1"),
    # },
    # "send_email_report": {
    #     "task": "user.tasks.send_email_report",
    #     "schedule": crontab(hour="*/1"),
    # },
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api/v1',
    'DEFAULT_GENERATOR_CLASS': 'drf_spectacular.generators.SchemaGenerator',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
    'COMPONENT_SPLIT_PATCH': True,
    'COMPONENT_SPLIT_REQUEST': True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "displayRequestDuration": True
    },
    'UPLOADED_FILES_USE_URL': True,
    'TITLE': APP_DESCRIPTION,
    'DESCRIPTION': f'{APP_DESCRIPTION} Doc',
    'VERSION': '1.0.0',
    'LICENCE': {'name': 'BSD License'},
    'CONTACT': {'name': 'Daniel Ale', 'email': 'd.ale@capitalsage.ng'},

    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flows-object
    'OAUTH2_FLOWS': [],
    'OAUTH2_AUTHORIZATION_URL': None,
    'OAUTH2_TOKEN_URL': None,
    'OAUTH2_REFRESH_URL': None,
    'OAUTH2_SCOPES': None,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

if DEBUG == 0:
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN', None),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

DOJAH_APP_ID = os.environ.get('DOJAH_APP_ID')
DOJAH_API_KEY = os.environ.get('DOJAH_API_KEY')
DEFAULT_IDENTITY_SERVICE = os.environ.get('DEFAULT_IDENTITY_SERVICE', 'DOJAH')
