from django.db.models.signals import post_save
from django.dispatch import receiver

from cvback.alerts.models import SubscribedEvent
from cvback.events.models import Event

from cvback.events.tasks import  create_alert
@receiver(post_save, sender=Event)
def post_save_event_handler(sender, instance, created, **kwargs):
    create_alert(instance)