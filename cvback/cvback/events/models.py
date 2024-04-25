from django.db import models
from django_jsonform.models.fields import ArrayField
from cvback.devices.models import Camera, InferenceComputer
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey


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

class Event(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    inference_detection_classification = models.ForeignKey('InferenceDetectionClassification', on_delete=models.CASCADE, null=True, blank=True)
    inference_classification = models.ForeignKey('InferenceClassification', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Event at {self.added_date} from {self.camera}"

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


    class Meta:
        abstract = True
    def __str__(self):
        return f"{self.inference_computer} > {self.added_date}"

class Label(models.Model):
    model = models.CharField(max_length=255)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label

class InferenceDetectionClassification(Inference):
    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return f"InferenceDetectionClassification ID: {self.id}"
     
    #Paula va a poner un validador que los bounding boxes sean la misma cantidad que los labels
    def clean(self):
        #Validate only if both ManyToMany relationships have been established
        if self.pk:
            if self.bounding_boxes.count() != self.labels.count():
                raise ValidationError("The number of bounding boxes must match the number of labels") #pag 146

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()


class InferenceClassification(Inference):
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date} > {self.label}"    


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
    related_event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='alerts') # Arreglar el loop weon

