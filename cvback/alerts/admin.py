from django.contrib import admin
from .models import Alert, SubscribedEvent, AlertType, Subscription

# Register your models here.
admin.site.register(Alert)
admin.site.register(SubscribedEvent)
admin.site.register(AlertType)
admin.site.register(Subscription)
