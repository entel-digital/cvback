from django.db import models
#from django.apps import apps
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
    related_event = models.ForeignKey('events.Event', on_delete=models.DO_NOTHING, related_name='alerts_from_alerts_unique')
