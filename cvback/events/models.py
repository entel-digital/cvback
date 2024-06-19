from django.db import models
from django_jsonform.models.fields import ArrayField
from cvback.devices.models import Camera, InferenceComputer

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import URLValidator


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
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.camera} > {self.name}"


class LineOfInterest(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    geometry = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    description = models.TextField(null=True, blank=True)


class Inference(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.DO_NOTHING)
    algorithm = models.ForeignKey('Algorithm', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date}"


class BoundingBox(Inference):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    top_left = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    bottom_right = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    color_label = models.CharField(max_length=30)
    # inference_class = models.CharField(max_length=255)
    # confidence = models.FloatField(validators=[validate_relative])
    # inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.CASCADE)


class TrackingID(Inference):
    pass
    # TODO: colores

class EventType(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    name = models.CharField(max_length=30)


class Event(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    cameras = models.ManyToManyField(Camera)

    inference_detection_classification = models.ForeignKey('InferenceDetectionClassification', on_delete=models.CASCADE, null=True, blank=True)
    inference_classification = models.ForeignKey('InferenceClassification', on_delete=models.CASCADE, null=True, blank=True)
    # TODO: crear clases vinculadas
    inference_detection_classification_tracker = models.ForeignKey('InferenceClassification', on_delete=models.CASCADE, null=True, blank=True)
    # inference_tracker
    # inference_ocr
    def __str__(self):
        return f"Event at {self.added_date} from {self.cameras}"


class Algorithm(models.Model):
    class AlgorithmKind(models.TextChoices):
        DETECTION_CLASSIFICATION_MODEL = 'detection_classification', 'Detection + classification model'
        DETECTION_CLASSIFICATION_TRACKING_MODEL = 'detection_classification_tracking', 'Detection + classification + tracking model'
        CLASSIFICATION_MODEL = 'classification', 'Classification model'
        CLASSIFICATION_CLASSIC_CV = 'cl_classification', 'Classification classic computer vision'
        BUSSINESS_LOGIC = ''

    kind = models.CharField(
           max_length=255,
           choices=AlgorithmKind.choices
    )
    added_date = models.DateTimeField("date created", auto_now_add=True)
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=30) # TODO: validate x.x.x format
    repository = models.CharField(max_length=30, validators=[URLValidator])


class Label(models.Model):
    class ColorGroup(models.TextChoices):
        PERSON = 'person'
        ANIMAL = 'animal'
        VEHICLE = 'vehicle'
        ID = 'id'
        PPE = 'ppe'
        OTHER = 'other'

    #model = models.CharField(max_length=255) # Para que el model?
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.label


class InferenceOCR(Inference):
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=255)
    # TODO: confidence acá y en todos


class InferenceDetectionClassification(Inference):
    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return f"InferenceDetectionClassification ID: {self.id}"

    def clean(self):
        if self.pk:
            if self.bounding_boxes.count() != self.labels.count():
                raise ValidationError("The number of bounding boxes must match the number of labels") #pag 146

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()

class InferenceDetectionClassificationTracker(Inference):
    tracking_ids = models.ManyToManyField(TrackingID)
    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return f"InferenceDetectionClassification ID: {self.id}"

    def clean(self):
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

