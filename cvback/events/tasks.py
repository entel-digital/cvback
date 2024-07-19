from celery import shared_task
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from cvback.events.serializers import EventSerializer
from django.utils import timezone
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender



@shared_task(rate_limit='100/m')            
def send_telegram(message,chat_id):
    telegram_sender = TelegramSender()
    telegram_sender.send_telegram(message, chat_id)

@shared_task(rate_limit='100/m')
def send_whatsapp(users_data,event_data):
    whatsapp_sender = WhatsappSender()
    token = whatsapp_sender.authenticate_whatsapp()
    whatsapp_sender.send_whatsapp(users_data,event_data,token )

def get_user_info(user):
    user_data = {"username":user.username, "phone_number":str(user.phone_number.country_code)+str(user.phone_number.national_number)}
    return user_data

def get_event_info(event):
    event_data = {}
    event_data["date"] = event.informed_date.strftime("%Y-%m-%d") if event.informed_date else ""
    event_data["time"] = event.informed_date.strftime('%H:%M:%S') if event.informed_date else ""
    if event.inference_ocr.all():
        if event.inference_ocr.all()[0].value:
            
            event_data["vehicle_license_plate"] = event.inference_ocr.all()[0].value
        else:
            event_data["vehicle_license_plate"] = ""
    else:
        event_data["vehicle_license_plate"] = ""
    event_data["missing_labels"] = [label.name for label in  event.labels_missing.all()] if  event.labels_missing.all() else []
    event_data["details_link"] =  "app-beta.sgscm.vision.enteldigital.cl"
    aux_images = [[frame.image for frame in kframe.frames.all()] for kframe in  event.key_frames.all()] if  event.key_frames.all() else []
    event_data["images"]= []
    [[event_data["images"].append(image) for image in images] for images in aux_images]
    return event_data



@shared_task(rate_limit='100/m')
def create_alert(event):
    message = f"{event.event_type}: {event.event_label} a las {event.informed_date}"
    new_alert = Alert(related_event=event, message=message)
    new_alert.save()
    subscribed_event = SubscribedEvent.objects.all()
    if subscribed_event:
        event_data = get_event_info(event)
        subscriptions = Subscription.objects.filter(suscribed_events=subscribed_event[0]).all()
        users_data = []
        for subscription in subscriptions:
            alert_types = [alert_type.channel for alert_type in subscription.alert_type.all()]
            if subscription.user.telegram_chat_id and "telegram" in alert_types:
                chat_id = subscription.user.telegram_chat_id
                send_telegram(message, chat_id)
            if subscription.user.phone_number and "whatsapp" in alert_types:
                users_data.append(get_user_info(subscription.user))
                
                
            if subscription.user.phone_number and subscription.alert_type.name=="sms":
                pass
        if users_data:
            send_whatsapp(users_data,event_data)