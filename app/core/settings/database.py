import os

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
