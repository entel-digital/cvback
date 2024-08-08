# import logging

from .base import *  # noqa
from .base import env

# TODO: set storage to google storage
# TODO: set cdn to "dome" (Entel's cloudflair)


# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["enteldigital.cl"])

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", None)
WHATSAPP_CLIENT_ID = env("WHATSAPP_CLIENT_ID", None)
WHATSAPP_CLIENT_SECRET = env("WHATSAPP_CLIENT_SECRET", None)
WHATSAPP_AUTHENTICATION_URL = env("WHATSAPP_AUTHENTICATION_URL", None)
WHATSAPP_SEND_MESSAGES_URL = env("WHATSAPP_SEND_MESSAGES_URL", None)
WHATSAPP_CAMPAIGN_ID = env("WHATSAPP_CAMPAIGN_ID", None)
WHATSAPP_TYPE_ACTION = env("WHATSAPP_TYPE_ACTION", None)

GRAPHIQL_GRAPHIC_INTERFACE = False

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa: F405

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": ""
    }
}
# CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": env("REDIS_URL"),
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#            Mimicing memcache behavior.
#            shttps://github.com/jazzband/django-redis#memcached-exceptions-behavior
#            "IGNORE_EXCEPTIONS": True,
#        },
#    }
# }

# SECURITY
# ------------------------------------------------------------------------------
# CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=["enteldigital.cl"])
# CSRF_ALLOWED_ORIGINS = env.list("DJANGO_CSRF_ALLOWED_ORIGINS", default=["enteldigital.cl"])
# CORS_ORIGINS_WHITELIST = env.list("DJANGO_CORS_ORIGINS_WHITELIST", default=["enteldigital.cl"])
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True)

# STORAGES
# ------------------------------------------------------------------------------
# https://django-storages.readthedocs.io/en/latest/#installation
# INSTALLED_APPS += ["storages"]  # noqa: F405
# GS_BUCKET_NAME = env("DJANGO_GCP_STORAGE_BUCKET_NAME")
# GS_DEFAULT_ACL = "publicRead"
# # STATIC
# # ------------------------
# STATICFILES_STORAGE = "cvback.utils.storages.StaticGoogleCloudStorage"
# COLLECTFAST_STRATEGY = "collectfast.strategies.gcloud.GoogleCloudStrategy"
# STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/static/"
# # MEDIA
# # ------------------------------------------------------------------------------
# DEFAULT_FILE_STORAGE = "cvback.utils.storages.MediaGoogleCloudStorage"
# MEDIA_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/media/"
STATIC_URL = "/static/"
# MEDIA_URL = "/media/"
DEBUG = False



# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="CVBack <noreply@enteldigital.cl>",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[CVBack] ",
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")

# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa: F405
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
# EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
# EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
EMAIL_BACKEND = "anymail.backends.mailjet.EmailBackend"
ANYMAIL = {
    "MAILJET_API_KEY": env("DJANGO_MAILJET_API_KEY"),
    "MAILJET_SECRET_KEY": env("DJANGO_MAILJET_SECRET_KEY"),
}

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": True,
#     "formatters": {
#         "verbose": {
#             "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         }
#     },
#     "root": {"level": "INFO", "handlers": ["console"]},
#     "loggers": {
#         "django.db.backends": {
#             "level": "ERROR",
#             "handlers": ["console"],
#             "propagate": False,
#         },
#         # Errors logged by the SDK itself
#         "sentry_sdk": {"level": "ERROR", "handlers": ["console"], "propagate": False},
#         "django.security.DisallowedHost": {
#             "level": "ERROR",
#             "handlers": ["console"],
#             "propagate": False,
#         },
#     },
# }

# Sentry
# ------------------------------------------------------------------------------
# SENTRY_DSN = env("SENTRY_DSN")
# SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

# sentry_logging = LoggingIntegration(
#     level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
#     event_level=logging.ERROR,  # Send errors as events
# )
# integrations = [sentry_logging, DjangoIntegration(), RedisIntegration()]
# sentry_sdk.init(
#     dsn=SENTRY_DSN,
#     integrations=integrations,
#     environment=env("SENTRY_ENVIRONMENT", default="production"),
#     traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
# )


# Your stuff...
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["corsheaders", "django_extensions"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += [  # noqa: F405
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.common.CommonMiddleware"
    ]  # noqa: F405

CORS_ORIGIN_ALLOW_ALL = True
