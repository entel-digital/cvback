from django.db import models
from django_jsonform.models.fields import ArrayField
#from django.contrib.postgres.fields import ArrayField
#from django_better_admin_arrayfield.models.fields import ArrayField
from devices.models import Camera, InferenceComputer
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
    # TODO: color?

    def __str__(self):
        return f"{self.camera} > {self.name}"

class BoundingBox(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    top_left = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    bottom_right = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    type = models.CharField(max_length=255)
    confidence = models.FloatField(validators=[validate_relative])

class Inference(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.DO_NOTHING)
    bounding_boxes = models.ForeignKey(BoundingBox, on_delete=models.DO_NOTHING)

class Event(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    inference = models.ForeignKey(Inference, on_delete=models.DO_NOTHING)

class TelegramAlert(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    telegram_user = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    events = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

class SMSAlert(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    phone_number = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    events = models.ForeignKey(Event, on_delete=models.DO_NOTHING)

