from celery import shared_task
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from cvback.events.serializers import EventSerializer
from django.utils import timezone
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender

@shared_task(rate_limit='100/m')            
def send_whatsapp(user,message):
    pass

@shared_task(rate_limit='100/m')            
def send_telegram(message,chat_id):
    telegram_sender = TelegramSender()
    print("send_telegram", message, chat_id)
    telegram_sender.send_telegram(message, chat_id)

@shared_task
def send_whatsapp(message,chat_id):
    pass
    whatsapp_sender = WhatsappSender()
    whatsapp_sender.authenticate_whatsapp()
    whatsapp_sender.send_whatsapp(message,chat_id)

@shared_task(rate_limit='100/m')
def create_alert(event):
    message = f"{event.event_type}: {event.event_label} a las {event.informed_date}"
    new_alert = Alert(related_event=event, message=message)
    new_alert.save()
    chat_id = '5861719546'
    chat_id = '-4266442874'
    send_telegram(message,chat_id)
    subscribed_event = SubscribedEvent.objects.all()
    if subscribed_event:
        subscriptions = Subscription.objects.filter(subscribed_event=subscribed_event).all()
        
        for subscription in subscriptions:
            if subscription.user.telegram_chat_id and subscription.alert_type.name=="telegram":
                chat_id = subscription.user.telegram_chat_id
                send_telegram(message, chat_id)
            if subscription.user.phone_number and subscription.alert_type.name=="whatsapp":
                chat_id = subscription.user.phone_number
                
                print('send_whatsapp(message, chat_id)')
            if subscription.user.phone_number and subscription.alert_type.name=="sms":
                pass

