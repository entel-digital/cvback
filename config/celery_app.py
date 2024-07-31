import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
if (os.getenv('PLATFORM_APPLICATION_NAME') is None):
    if (os.getenv('CVBACK_PRODUCTION') == 'True'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.platform")

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("cvback")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
