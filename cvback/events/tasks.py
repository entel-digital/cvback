from celery import shared_task
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from django.utils import timezone
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender
from functools import reduce

@shared_task(rate_limit='100/m')            
def send_telegram(message,chat_id,image_url=None):
    telegram_sender = TelegramSender()
    telegram_sender.send_telegram(message, chat_id,image_url)

@shared_task(rate_limit='100/m')            
def send_whatsapp(users_data,event_data):
    if not users_data:
        return
    whatsapp_sender = WhatsappSender()
    token = whatsapp_sender.authenticate_whatsapp()
    whatsapp_sender.send_whatsapp(users_data,token, event_data)

@shared_task(rate_limit='100/m')
def create_alert(event):
    
    message = f"{event.event_type}: {event.event_label} a las {event.informed_date}"
    new_alert = Alert(related_event=event, message=message)
    new_alert.save()
    subscribed_event = SubscribedEvent.objects.filter(event_type=event.event_type, event_label=event.event_label).first()
    if subscribed_event:
        images = [[f.image for f in kf.frames.all() if f.image] for kf in  event.key_frames.all()]      
        images = list(reduce(lambda x, y: x + y, images, []))
        event_data ={ "date":event.informed_date.strftime('%Y-%m-%d'),
                      "time":event.informed_date.strftime('%H:%M:%S'),
                      "vehicle_licence_plate":event.inference_ocr.first().value if event.inference_ocr.first() else '',
                      "missing_labels":', '.join([label.name for label in event.labels_missing.all()]) if event.labels_missing.all() else '',
                      "details_link":"...",
                      "images":images if images else ['']}

        subscriptions = Subscription.objects.filter(suscribed_events=subscribed_event)
        users_data = []
        for subscription in subscriptions:
            channels = [c.channel for c in subscription.alert_type.all()]
            if subscription.user.telegram_chat_id and "telegram" in channels:
                chat_id = subscription.user.telegram_chat_id
                send_telegram(message, chat_id)
            if subscription.user.phone_number and "whatsapp" in channels:
                users_data.append({"phone_number":subscription.user.phone_number.raw_input[1:],"username":subscription.user.username,"priority":subscription.priority})
                
            if subscription.user.phone_number and "sms" in channels:
                pass
        if users_data:
            users_data.sort(key=lambda x: x["priority"])
            send_whatsapp(users_data,event_data)
