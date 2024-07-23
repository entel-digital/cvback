from celery import shared_task
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender
from django.utils import timezone
from django.db import connections

to_tz = timezone.get_default_timezone()

@shared_task(rate_limit='100/m')            
def send_telegram(message,chat_id,images):
    telegram_sender = TelegramSender()
    telegram_sender.send_telegram(message, chat_id, images)

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
    informed_date = event.informed_date.astimezone(to_tz).strftime("%Y-%m-%d")
    informed_time = event.informed_date.astimezone(to_tz).strftime("%H:%M:%S")
    event_data["date"] = informed_date if event.informed_date else ""
    event_data["time"] = informed_time if event.informed_date else ""
    if event.inference_ocr.all():
        if event.inference_ocr.all()[0].value:

            event_data["vehicle_license_plate"] = event.inference_ocr.all()[0].value
        else:
            event_data["vehicle_license_plate"] = ""
    else:
        event_data["vehicle_license_plate"] = ""
    event_data["missing_labels"] = [label.name for label in  event.labels_missing.all()] if  event.labels_missing.all() else []
    #event_data["details_link"] =  "app-beta.sgscm.vision.enteldigital.cl"
    event_data["details_link"] =  f"https://app-beta.sgscm.vision.enteldigital.cl/kTdTNssbOrlOBTyv4gYWZeaYqY06K5IC/events/event/{event.id}/change/"
    
    aux_images = [[frame.image for frame in kframe.frames.all()] for kframe in  event.key_frames.all()] if  event.key_frames.all() else []
    event_data["images"]= []
    [[event_data["images"].append(image.url) for image in images] for images in aux_images]
    return event_data


def select_subscribed_events(event_type, event_label):
    
    qs_et = SubscribedEvent.objects.filter(event_type=event_type) 
    
    qs_el = SubscribedEvent.objects.filter(event_label=event_label)
    qs = qs_et.intersection(qs_el).all()
    return qs

def filter_subscriptions(subscribed_events):
    qs = Subscription.objects.none()
    for subscribed_event in subscribed_events:
        qs = qs.union(Subscription.objects.filter(suscribed_events=subscribed_event)).all()
    return qs
    

@shared_task(rate_limit='100/m')
def create_alert(event):
    message = f"{event.event_type}: {event.event_label} a las {event.informed_date.astimezone(to_tz)}"
    new_alert = Alert(related_event=event, message=message)
    new_alert.save()
    subscribed_event = select_subscribed_events(event.event_type,event.event_label)
    if subscribed_event:
        event_data = get_event_info(event)
        subscriptions = filter_subscriptions(subscribed_event)
        users_data = []
        for subscription in subscriptions:
            alert_types = [alert_type.channel for alert_type in subscription.alert_type.all()]
            if subscription.user.telegram_chat_id and "telegram" in alert_types:
                chat_id = subscription.user.telegram_chat_id
                send_telegram(message, chat_id,event_data["images"])
            if subscription.user.phone_number and "whatsapp" in alert_types:
                users_data.append(get_user_info(subscription.user))
            if subscription.user.phone_number and subscription.alert_type.name=="sms":
                pass
        if users_data:
            send_whatsapp(users_data,event_data)
    