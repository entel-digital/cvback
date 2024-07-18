from django.db import models
#from django.apps import apps
from cvback.events.models import Event, EventType, Label
from cvback.users.models import User

class Alert(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    message = models.CharField(max_length=255)
    related_event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='alerts_from_alerts_unique')


class SubscribedEvent(models.Model):
    name = models.CharField()
    event_type = models.ManyToManyField(EventType)
    event_label = models.ManyToManyField(Label)

class AlertType(models.Model):
    channel=models.CharField(max_length=50)

class Subscription(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    alert_type = models.ManyToManyField(AlertType)
    suscribed_events = models.ManyToManyField(SubscribedEvent)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users_from_suscription")
    priority = models.IntegerField()
    # TODO: ver turnos



# TODO: https://www.geeksforgeeks.org/send-message-to-telegram-user-using-python/
