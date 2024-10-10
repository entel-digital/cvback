from datetime import datetime
from celery import shared_task
from django.conf import settings
import pandas as pd
from cvback.alerts.models import Alert, SubscribedEvent, Subscription
from cvback.events.models import Event, ExportedFile
from cvback.users.adapters import AccountAdapter
from cvback.utils.telegram_sender import TelegramSender
from cvback.utils.whatsapp_sender import WhatsappSender
from django.utils import timezone
from cvback.utils.storages import MediaGoogleCloudStorage
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
    event_data["event_label"] = event.event_label.name.capitalize() if event.event_label.name else ""
    if event.inference_ocr.all():
        if event.inference_ocr.all()[0].value:
            event_data["vehicle_license_plate"] = event.inference_ocr.all()[0].value
        else:
            event_data["vehicle_license_plate"] = ""
    else:
        event_data["vehicle_license_plate"] = ""
    missing_labels = event.labels_missing.all()
    event_data["missing_labels"] = [label.name for label in event.labels_missing.all()] if missing_labels else []
    link = "https://app.sgscm.vision.enteldigital.cl/kTdTNssbOrlOBTyv4gYWZeaYqY06K5IC42/"
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
                send_telegram.delay(chat_id, event_data)
            if subscription.user.phone_number and "whatsapp" in alert_types:
                users_data.append(get_user_info(subscription.user))
            if subscription.user.phone_number and subscription.alert_type.name == "sms":
                pass
        if users_data:
            send_whatsapp.delay(users_data, event_data)


@shared_task(rate_limit='100/m', time_limit=3600)
def save_file(request_username, request_email, full_data, format, id_equals_to, date_equals_to, date_lower_than, date_greater_than_equal, label_id_filter, sorted_by, asc):
    
    qs = Event.objects.all()

    FORMATS = ["CSV", "XLSX"]
    if not format in FORMATS:
        format = "CSV"

    if sorted_by:
        sort_param=sorted_by
        if not asc:
            sort_param="-"+sort_param
        qs = qs.order_by(sort_param) 
         
    if label_id_filter:
        qs = qs.filter(event_label__id=label_id_filter)
    if id_equals_to:
        qs = qs.filter(id=id_equals_to)
    if date_equals_to:
        qs = qs.filter(informed_date=date_equals_to)
    if date_lower_than:
        qs = qs.filter(informed_date__lt=date_lower_than)
    if date_greater_than_equal:
        qs = qs.filter(informed_date__gte=date_greater_than_equal)

    if full_data:
        field_names = settings.EXPORT_FULL_CSV_FIELDS
    else:
        field_names = settings.EXPORT_SUMMARY_CSV_FIELDS

    if not format in ["CSV", "XLSX"]:
        format = "CSV"

    return_file = IO()


    EXPORT_GROUP_BY = [c for c in field_names if c in settings.EXPORT_GROUP_BY]
    EXPORT_TO_AGGREGATE_FIELD = [c for c in field_names if c in settings.EXPORT_TO_AGGREGATE]
    
    field_names = [f if "*" not in f else f.split("*")[0] for f in field_names]
    df = pd.DataFrame(qs.values(*field_names).iterator())
    aggregation_fields = {}
    for_get_url = []
    for field in EXPORT_TO_AGGREGATE_FIELD:
        if not "*" in field:
            key = field
        else:
            key = field.split("*")[0]
            
            for_get_url.append(key)
        aggregation_fields[key] = set
    
    df = df.groupby(EXPORT_GROUP_BY, as_index = False).agg(aggregation_fields)  
    
    storage = MediaGoogleCloudStorage()
    for col in for_get_url:
        df[col] = df[col].apply(lambda x: concat_urls(x,storage))
    if not full_data:
        for trans_parameters in settings.EXPORT_DICTS_TO_TRANSFORM_COLUMNS:
            t_dict =  trans_parameters["transformations"]
            if trans_parameters["type_transform"] == "in":
                df[trans_parameters["column_base"]] = df[trans_parameters["column_base"]].apply(lambda x: in_transformation(x,t_dict))
                df = df.rename(columns={trans_parameters["column_base"]:trans_parameters["column_name"]})
            elif trans_parameters["type_transform"] == "replace":
                df[trans_parameters["column_base"]] = df[trans_parameters["column_base"]].apply(lambda x: replace_transformation(x,t_dict))
            if not trans_parameters["keep_base"]:
                df = df.drop([trans_parameters["column_base"]], axis=1) 
                
        df = df.rename(columns=settings.EXPORT_TRANSLATION_SUMMARY_FIELDS)
    filename = get_filename(qs)

    if format == "XLSX":
        filename = filename.replace(".csv","")
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"
        date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
        for date_column in date_columns:
            df[date_column] = df[date_column].dt.tz_convert(settings.TIME_ZONE).dt.strftime('%Y-%m-%d %H:%M:%S')
        with pd.ExcelWriter(return_file, engine='openpyxl', datetime_format= "dd-mm-yy hh:mm:ss") as writer:
            df.to_excel(writer, sheet_name=settings.XLSX_SHEET_NAME, index=False)

    elif format == "CSV":
        mime_type="text/csv"
        date_columns = df.select_dtypes(include=['datetime64[ns, UTC]']).columns
        for date_column in date_columns:
            df[date_column] = df[date_column].dt.tz_convert(settings.TIME_ZONE)#.dt.to_timestamp()
        filename = filename.replace(".xlsx","")
        if not filename.endswith(".csv"):
            filename += ".csv"
        df.to_csv(return_file, index=False, date_format='%Y-%m-%d %H:%M:%S')
        
    exported_file = ExportedFile()
    exported_file.exported_file.save("./"+filename, return_file)
    exported_file.save()
    public_uri = exported_file.exported_file.url
    context = {"public_uri":public_uri, "username":request_username, "filename":filename }#, "mime_type":mime_type, "file":exported_file.exported_file.open().read()}
    if public_uri:
        r = AccountAdapter().send_mail_( template_prefix="account/custom_email/email_csv_ready",
                                        email=request_email,
                                        context=context,
                                        request="request")
    else:
        
        r = AccountAdapter().send_mail_( template_prefix="account/custom_email/email_csv_failed",
                                        email=request_email,
                                        context=context,
                                        request="request")


def in_transformation(x,t_dict):
    for k in t_dict:
        if k.lower() in [l.lower() for l in x]:
            return t_dict[k]
    return "-"

def replace_transformation(x, t_dict):
    if isinstance(x,set):
        nx = list(x)
        nx = ",".join([ t_dict.get(y,"-") for y in nx ])
        return nx
    print("the x", x)
    return t_dict.get(x,"-")

def get_filename(queryset):
        return "data-export-{!s}".format(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))


def concat_urls(x,storage):
    urls_set =  {storage.url(name=y) if y else "" for y in x}

    return '\r\n'.join(list(urls_set))