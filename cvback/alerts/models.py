from django.db import models
from cvback.events.models import Event
# Create your models here.
class Alert(models.Model):
    ALERT_TYPES = (
        ('telegram', 'Telegram'),
        ('sms', 'SMS'),
        ('whatsapp_group', 'Whatsapp group'),
    )
    added_date = models.DateTimeField("date created", auto_now_add=True)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    recipient = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    related_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='alerts')
