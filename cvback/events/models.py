from django.db import models
from django_jsonform.models.fields import ArrayField
#from django.contrib.postgres.fields import ArrayField
#from django_better_admin_arrayfield.models.fields import ArrayField
from cvback.devices.models import Camera, InferenceComputer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_relative(value):
    if value < 0 or value > 1:
        raise ValidationError(
            _("%(value)s not between 0 and 1. We use relative areas of interest"),
            params={"value": value},
        )

class AreaOfInterest(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    geometry = ArrayField(ArrayField(models.FloatField(validators=[validate_relative]), size=2))
    description = models.TextField(null=True, blank=True) ## validar TODO: color?

    def __str__(self):
        return f"{self.camera} > {self.name}"

class BoundingBox(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    top_left = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    bottom_right = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    type = models.CharField(max_length=255)
    confidence = models.FloatField(validators=[validate_relative])
    #related_event = models.ForeignKey('Event', null=True, on_delete=models.CASCADE, related_name='bounding_boxes') ## Validar


class Inference(models.Model):
    class InferenceKind(models.TextChoices):
        DETECTION_PLUS_CLASSIFICATION = 'dc', 'Detection + classification'
        CLASSIFICATION = 'cl', 'Classification'

    kind = models.CharField(
           max_length=2,
           choices=InferenceKind.choices
    )
    added_date = models.DateTimeField("date created", auto_now_add=True)
    inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.DO_NOTHING)
    #related_event = models.ForeignKey('Event', null=True, on_delete=models.CASCADE, related_name='inferences') ## Validar

    class Meta:
        abstract = True
    def __str__(self):
        return f"{self.inference_computer} > {self.added_date}"

class Label(models.Model):
    model = models.CharField()
    label = models.CharField()

    def __str__(self):
        return self.label


class InferenceDetectionClassification(Inference):
    def __init__(self):
        super().__init__()

    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)

    # TODO: Paula va a poner un validador que los bounding boxes sean la misma cantidad que los labels

    # Pseudo code (la Paula lo va a arreglar)
    def __str__(self):
        if len(self.labels) >= 1:
            return f"{self.inference_computer} > {self.added_date} > {self.labels[0]}"
        else:
            return f"{self.inference_computer} > {self.added_date}"


class InferenceClassification(Inference):
    def __init__(self):
        super().__init__()

    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date} > {self.label}"


class Event(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    inference = models.ForeignKey(Inference, on_delete=models.DO_NOTHING)
    #type = models.CharField(max_length=255) #Qué tipo de evento
    #tag = models.CharField(max_length=50) # Etiquetar eventos??


class Alert(models.Model): # Validar clase
    ALERT_TYPES = (
        ('telegram', 'Telegram'),
        ('sms', 'SMS'),
        ('whatsapp_group', 'Whatsapp group'),
    )
    added_date = models.DateTimeField("date created", auto_now_add=True)
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    recipient = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    related_event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name='alerts')


"""class TelegramAlert(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    telegram_user = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    events = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

class SMSAlert(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    phone_number = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    events = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

"""
