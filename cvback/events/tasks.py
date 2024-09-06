from celery import shared_task
import pandas as pd
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from cvback.events.models import ExportedFile
from cvback.users.adapters import AccountAdapter
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender
from django.utils import timezone

from io import BytesIO as IO


to_tz = timezone.get_default_timezone()


@shared_task(rate_limit='100/m')
def send_telegram(chat_id, event_data):
    telegram_sender = TelegramSender()
    telegram_sender.send_telegram(chat_id, event_data)


@shared_task(rate_limit='100/m')
def send_whatsapp(users_data, event_data):
    whatsapp_sender = WhatsappSender()
    token = whatsapp_sender.authenticate_whatsapp()
    whatsapp_sender.send_whatsapp(users_data, event_data, token)


def get_user_info(user):
    user_data = {"username": user.username,
                 "phone_number": str(user.phone_number.country_code)+str(user.phone_number.national_number)}
    return user_data


def get_event_info(event):
    event_data = {}
    informed_date = event.informed_date.astimezone(to_tz).strftime("%Y-%m-%d")
    informed_time = event.informed_date.astimezone(to_tz).strftime("%H:%M:%S")
    event_data["id"] = event.id
    event_data["date"] = informed_date if event.informed_date else ""
    event_data["time"] = informed_time if event.informed_date else ""
    event_data["event_label"] = event.event_label.name
    if event.inference_ocr.all():
        if event.inference_ocr.all()[0].value:
            event_data["vehicle_license_plate"] = event.inference_ocr.all()[0].value
        else:
            event_data["vehicle_license_plate"] = ""
    else:
        event_data["vehicle_license_plate"] = ""
    missing_labels = event.labels_missing.all()
    event_data["missing_labels"] = [label.name for label in event.labels_missing.all()] if missing_labels else []
    link = "https://app-beta.sgscm.vision.enteldigital.cl/kTdTNssbOrlOBTyv4gYWZeaYqY06K5IC/"
    link += f"events/event/{event.id}/change/"
    event_data["details_link"] = link

    aux_images = [[frame.image for frame in kframe.frames.all()]
                  for kframe in event.key_frames.all()] if event.key_frames.all() else []
    event_data["images"] = []
    [[event_data["images"].append(image.url) for image in images] for images in aux_images]

    aux_videos = [[video.video for video in kvideo.videos.all()]
                  for kvideo in event.key_videos.all()] if event.key_videos.all() else []

    event_data["videos"] = []
    [[event_data["videos"].append(video.url) for video in videos] for videos in aux_videos]
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
    subscribed_event = select_subscribed_events(event.event_type, event.event_label)
    if subscribed_event:
        event_data = get_event_info(event)
        subscriptions = filter_subscriptions(subscribed_event)
        users_data = []
        for subscription in subscriptions:
            alert_types = [alert_type.channel for alert_type in subscription.alert_type.all()]
            if subscription.user.telegram_chat_id and "telegram" in alert_types:
                chat_id = subscription.user.telegram_chat_id
                send_telegram(chat_id, event_data)
            if subscription.user.phone_number and "whatsapp" in alert_types:
                users_data.append(get_user_info(subscription.user))
            if subscription.user.phone_number and subscription.alert_type.name == "sms":
                pass
        if users_data:
            send_whatsapp(users_data, event_data)


@shared_task(rate_limit='4/h')
def save_file(qs,field_names, cls, request, format ):

    filename = cls.get_filename(qs)
    if not format in ["CSV", "XLSX"]:
        format = "CSV"
    return_file = IO()

    df = pd.DataFrame(qs.values(*field_names))
    filename = cls.get_filename(qs)
    if format == "XLSX":
        filename = filename.replace(".csv","")
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        writer = pd.ExcelWriter(return_file, engine='xlsxwriter')

        date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
        for date_column in date_columns:
            df[date_column] = df[date_column].dt.date
        mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

        df.to_excel(writer, 'EVENTS')

        
    elif format == "CSV":
        mime_type="text/csv"
        filename = filename.replace(".xlsx","")
        if not filename.endswith(".csv"):
            filename += ".csv"
        df.to_csv(return_file)
        
    exported_file = ExportedFile()
    exported_file.exported_file.save("./"+filename, return_file)
    exported_file.save()

    public_uri = exported_file.exported_file.url
    
    context = {"public_uri":public_uri, "username":request.user.username, "filename":filename, "mime_type":mime_type, "file":return_file}
    if public_uri:

        r = AccountAdapter().send_mail_( template_prefix="account/custom_email/email_csv_ready",
                                        email=request.user.email,
                                        context=context,
                                        request=request)
        
    else:
        
        r = AccountAdapter().send_mail_( template_prefix="account/custom_email/email_csv_failed",
                                        email=request.user.email,
                                        context=context,
                                        request=request)
