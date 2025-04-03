import logging
import os
import socket
from datetime import timedelta
from email.headerregistry import Address
from pathlib import Path

import hvac
import sentry_sdk
from celery.schedules import crontab
from corsheaders.defaults import default_headers
from kombu import Exchange, Queue
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

vault_client = hvac.Client(
    url=os.environ.get("ATHENA_VAULT_URL"),
    token=os.environ.get("ATHENA_VAULT_TOKEN"),
)

vault_keys = vault_client.secrets.kv.read_secret_version(
    path=os.environ.get("ATHENA_VAULT_KEY")
)["data"]["data"]

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = vault_keys["SECRET_KEY"]
DEBUG = int(os.environ.get("DEBUG", 1))
APP_DESCRIPTION = os.environ.get("APP_DESCRIPTION", "Phlox Wallet API")

ALLOWED_HOSTS = [
    "127.0.0.1",
    "0.0.0.0",
    "localhost",
    "api",
    "host.docker.internal",
]
INTERNAL_IPS = ["127.0.0.1"]
if DEBUG:
    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[:-1] + "1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "storages",
    "rest_framework",
    "rest_framework_api_key",
    "django_filters",
    "import_export",
    "debug_toolbar",
    "drf_spectacular",
    "django_extensions",
    "django_celery_beat",
    "core.celery.CeleryConfig",
    # "pykolofinance",
    "user.apps.UserConfig",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.ValidationErrorMiddleware",
    "core.middleware.RequestResponseLoggerMiddleware",
    # "pykolofinance.audtilog.logger.APILoggerMiddleware",
]

AUTH_USER_MODEL = "user.User"
ROOT_URLCONF = "core.urls"
IMPORT_EXPORT_USE_TRANSACTIONS = True

SAFE_LIST_IPS = os.getenv("SAFE_LIST_IPS", "").split(",")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "https://*.cintrustmfb.com",
    "https://wallet-api.phlox.st.sageitops.com",
    "https://api.wallet.phlox.kolomonimfb.com",
]
CORS_ALLOW_HEADERS = list(default_headers) + ["X-KMS-TOKEN", "X-Api-Key"]
LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

JAZZMIN_SETTINGS = {
    "site_title": APP_DESCRIPTION,
    "site_header": APP_DESCRIPTION,
}

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PORT": os.environ.get("POSTGRES_PORT"),
    },
    # "audit": {
    #     "ENGINE": "django.db.backends.postgresql_psycopg2",
    #     "NAME": os.environ.get("KAMS_POSTGRES_DB"),
    #     "USER": os.environ.get("KAMS_POSTGRES_USER"),
    #     "PASSWORD": os.environ.get("KAMS_POSTGRES_PASSWORD"),
    #     "HOST": os.environ.get("KAMS_POSTGRES_HOST"),
    #     "PORT": os.environ.get("KAMS_POSTGRES_PORT"),
    #     "CONN_MAX_AGE": 3600,
    # },
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Lagos"
USE_I18N = True
USE_TZ = True

DATE_INPUT_FORMATS = [
    "%d/%m/%Y",
    "%d/%m/%y",  # '10/02/2020', '10/02/20'
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%m/%d/%y",  # '2006-10-25', '10/25/2006', '10/25/06'
    "%b %d %Y",
    "%b %d, %Y",  # 'Oct 25 2006', 'Oct 25, 2006'
    "%d %b %Y",
    "%d %b, %Y",  # '25 Oct 2006', '25 Oct, 2006'
    "%B %d %Y",
    "%B %d, %Y",  # 'October 25, 2006', 'October 25, 2006'
    "%d %B %Y",
    "%d %B, %Y",  # '25 October 2006', '25 October 2006'
]

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "common.pagination.CustomPagination",
    "PAGE_SIZE": 12,
    # 'DATE_INPUT_FORMATS': ["%d/%m/%Y", ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/


APP_NAME = os.getenv("APP_NAME")
STATIC_LOCATION = f"{APP_NAME}/static"
MEDIA_LOCATION = f"{APP_NAME}/media"
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_ADDRESSING_STYLE = "virtual"
AWS_ACCESS_KEY_ID = vault_keys["ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = vault_keys["ACCESS_SECRET"]
AWS_STORAGE_BUCKET_NAME = vault_keys["BUCKET_NAME"]
AWS_S3_REGION_NAME = vault_keys["REGION_NAME"]
AWS_S3_ENDPOINT_URL = f"https://{AWS_S3_REGION_NAME}.digitaloceanspaces.com"
AWS_S3_CUSTOM_DOMAIN = vault_keys["CUSTOM_DOMAIN"]
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
AWS_LOCATION = STATIC_LOCATION
STATIC_URL = f"https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/"
# public media settings
PUBLIC_MEDIA_LOCATION = MEDIA_LOCATION
MEDIA_URL = f"https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"

IMPORT_EXPORT_TMP_STORAGE_CLASS = "import_export.tmp_storages.MediaStorage"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "location": AWS_LOCATION,
            "default_acl": AWS_DEFAULT_ACL,
            "object_parameters": {
                "CacheControl": "max-age=86400",
            },
        },
    },
    "staticfiles": {"BACKEND": "storages.backends.s3.S3Storage"},
    "import_export": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "region_name": AWS_S3_REGION_NAME,
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
        },
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "format": '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", '
            '"module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(asctime)s:%(log_color)s%(levelname)s:%(name)s:%(message)s ------------",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "verbose": {
            "format": (
                "\n--- %(levelname)s ---\n"
                "Timestamp: %(asctime)s\n"
                "Message: %(message)s\n"
                "Location: %(pathname)s:%(lineno)d in %(funcName)s\n"
                "-------------------------------------------------\n"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
        "opensearch": {
            "level": "ERROR",
            "class": "core.loghandler.OpenSearchLogHandler",  # Use Celery for logging
            "formatter": "json",
        },
    },
    "loggers": {
        # Catch all Django-related logs here
        "django": {
            "handlers": ["console", "opensearch"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    # Root logger for all other logs
    "root": {
        "handlers": ["console", "opensearch"],
        "level": "INFO",
    },
}

EMAIL_FROM = Address(
    display_name="Kolomoni MFB", addr_spec=os.environ.get("SENDER_EMAIL")
)
EMAIL_HOST = os.environ.get("SMTP_HOST")
EMAIL_HOST_USER = os.environ.get("SMTP_USER")
EMAIL_HOST_PASSWORD = os.environ.get("SMTP_PASSWORD")
EMAIL_PORT = os.environ.get("SMTP_PORT", 587)
EMAIL_USE_TLS = True

CLIENT_URL = os.environ.get("CLIENT_URL")
TOKEN_LIFESPAN = 24 * 7  # hours

REDIS_URL = os.getenv("REDIS_URL", "localhost:6379")

CELERY_RESULT_BACKEND = REDIS_URL
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_RESULT_EXPIRES = 18000

CELERY_QUEUES = (Queue("reversal_queue", Exchange("reversal"), routing_key="reversal"),)
CELERY_ROUTES = {
    "transaction.tasks.reverse_transaction_task": {"queue": "reversal_queue"},
}

CELERY_TASK_DEFAULT_QUEUE = "default"

FLOWER_BASIC_AUTH = os.environ.get("FLOWER_BASIC_AUTH")
# Assumes that the username is swift or simple have the url as redis://swift:jetSwift@localhost:6379/0
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": APP_NAME,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHE_TTL = 60 * 1
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [REDIS_URL],
        },
        # 'ROUTING': 'core'
    },
}

CELERY_BEAT_SCHEDULE = {
    "run_terminal_auto_debit": {
        "task": "wallet.tasks.run_auto_debit_process",
        "schedule": crontab(minute="0", hour="0", day_of_month="*"),
    }
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    },
}

SPECTACULAR_SETTINGS = {
    "SCHEMA_PATH_PREFIX": r"/api/v1",
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "COMPONENT_SPLIT_PATCH": True,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "displayRequestDuration": True,
    },
    "UPLOADED_FILES_USE_URL": True,
    "TITLE": APP_DESCRIPTION,
    "DESCRIPTION": f"{APP_DESCRIPTION} Doc",
    "VERSION": "1.0.0",
    "LICENCE": {"name": "BSD License"},
    "CONTACT": {"name": "Daniel Ale", "email": "d.ale@capitalsage.ng"},
    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flows-object
    "OAUTH2_FLOWS": [],
    "OAUTH2_AUTHORIZATION_URL": None,
    "OAUTH2_TOKEN_URL": None,
    "OAUTH2_REFRESH_URL": None,
    "OAUTH2_SCOPES": None,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=14),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

if not DEBUG:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(level=logging.ERROR, event_level=logging.ERROR),
        ],
        traces_sample_rate=1.0,
        send_default_pii=False,
        environment=os.environ.get("ENVIRONMENT_INSTANCE"),
    )

DRF_API_LOGGER_EXCLUDE_KEYS = [
    "tx_pin",
    "bvn",
    "nin",
    "X-KMS-KEY",
    "Authorization",
    "transaction_pin",
]
MONGODB_LOGGER_URL = vault_keys["MONGODB_LOGGER_URL"]
MONGODB_LOGGER_DATABASE = "app"

ENVIRONMENT_INSTANCE = os.environ.get("ENVIRONMENT_INSTANCE", "dev")
VANSO_SYSID = vault_keys["VANSO_SYSID"]
VANSO_PASSWORD = vault_keys["VANSO_PASSWORD"]
VANSO_SENDER = vault_keys["VANSO_SENDER"]
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"
