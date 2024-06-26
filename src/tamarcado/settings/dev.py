from src.tamarcado.settings.base import *  # noqa

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}

LOGGING = {
    **LOGGING,  # noqa
    "loggers": {
        "": {
            "level": "DEBUG",
            "handler": ['console','file']
        },
    },
}
