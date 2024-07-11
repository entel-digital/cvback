from django.contrib import admin
from .models import Alert, AlertType, SubscribedEvent, Subscription

# Register your models here.
admin.site.register(Alert)
admin.site.register(AlertType)
admin.site.register(SubscribedEvent)
admin.site.register(Subscription)
