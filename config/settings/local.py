from .base import *  # noqa
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="DRPsXxciYugvCPcalIjU4KZziYkdR2Ef10zDdZ1BDE43LBY1fIsctYgipI9vvVQ9",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]

# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": ""
    }
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar", "corsheaders"]  # noqa: F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += [  # noqa: F405
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.common.BrokenLinkEmailsMiddleware"
    ]  # noqa: F405

CORS_ALLOW_ALL_ORIGINS = True

# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2", "192.168.65.1"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]  # noqa: F405

# Your stuff...
# ------------------------------------------------------------------------------
# GDAL_LIBRARY_PATH = '/usr/local/Cellar/gdal/3.8.1_1/lib/libgdal.dylib'

#TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN", None)
#WHATSAPP_CLIENT_ID = env("WHATSAPP_CLIENT_ID", None)
#WHATSAPP_CLIENT_SECRET = env("WHATSAPP_CLIENT_SECRET", None)
#WHATSAPP_AUTHENTICATION_URL = env("WHATSAPP_AUTHENTICATION_URL", None)
#WHATSAPP_SEND_MESSAGES_URL = env("WHATSAPP_SEND_MESSAGES_URL", None)
#WHATSAPP_CAMPAIGN_ID = env("WHATSAPP_CAMPAIGN_ID", None)
#WHATSAPP_TYPE_ACTION = env("WHATSAPP_TYPE_ACTION", None)
GRAPHIQL_GRAPHIC_INTERFACE = True
