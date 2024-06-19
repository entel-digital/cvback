from django.db import models
from django_jsonform.models.fields import ArrayField
from cvback.devices.models import Camera, InferenceComputer

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.validators import URLValidator
#Quizás hacer una nueva aplicación tipo "inference" para simplificar el archivo

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

# TODO: Módulo para guardar historial... Field
class LineOfInterest(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    geometry = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    description = models.TextField(null=True, blank=True)


class Algorithm(models.Model):
    class AlgorithmKind(models.TextChoices):
        DETECTION_CLASSIFICATION_MODEL = 'detection_classification', 'Detection + classification model'
        DETECTION_CLASSIFICATION_TRACKING_MODEL = 'detection_classification_tracking', 'Detection + classification + tracking model'
        CLASSIFICATION_MODEL = 'classification', 'Classification model'
        CLASSIFICATION_CLASSIC_CV = 'cl_classification', 'Classification classic computer vision'
        BUSINESS_LOGIC = 'business_logic', 'Custom business logic'

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

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.label


class Frame(models.Model):
    image = models.FileField() # TODO: optional
    cameras = models.ManyToManyField(Camera)


class Video(models.Model):
    video = models.FileField()
    cameras = models.ManyToManyField(Camera)


class KeyFrames(models.Model):
    name = models.CharField()
    frames = models.ManyToManyField(Frame)


class KeyVideos(models.Model):
    name = models.CharField()
    frames = models.ManyToManyField(Video)


class Inference(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.DO_NOTHING)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, null=True, blank=True)
    confidence = models.FloatField(validators=[validate_relative])

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date}"


class BoundingBox(Inference):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    top_left = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    bottom_right = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    color_label = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Bounding boxes"


class InferenceOCR(Inference):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255) # TODO: un campo de texto más grande
    confidence = models.FloatField(validators=[validate_relative])


class KeyInferenceOCR(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceOCR, on_delete=models.CASCADE)


class InferenceDetectionClassification(Inference):
    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return f"InferenceDetectionClassification ID: {self.id}"

    def clean(self):
        if self.pk:
            if self.bounding_boxes.count() != self.labels.count():
                raise ValidationError("The number of bounding boxes must match the number of labels")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()


class KeyInferenceDetectionClassification(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceDetectionClassification, on_delete=models.CASCADE)


class InferenceDetectionClassificationTracker(Inference):
    tracking_ids = ArrayField(models.IntegerField())
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


class KeyInferenceDetectionClassificationTracker(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceDetectionClassificationTracker, on_delete=models.CASCADE)


class InferenceClassification(Inference):
    label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date} > {self.label}"


class KeyInferenceClassification(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceClassification, on_delete=models.DO_NOTHING)


class EventType(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=30) # TODO: validate x.x.x format


class Event(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    cameras = models.ManyToManyField(Camera)
    frames = models.ManyToManyField(Frame)
    key_frames = models.ManyToManyField(KeyFrames)
    videos = models.ManyToManyField(Video)
    key_videos = models.ManyToManyField(KeyVideos)
    confidence = models.FloatField(validators=[validate_relative], null=True, blank=True)
    labels_detected = models.ManyToManyField(Label, related_name='events_detected')
    labels_missing = models.ManyToManyField(Label, related_name='events_missing')

    # Inferences
    inference_classification = models.ManyToManyField(InferenceClassification, blank=True)
    inference_detection_classification = models.ForeignKey(InferenceDetectionClassification, on_delete=models.CASCADE, null=True, blank=True)
    inference_detection_classification_tracker = models.ManyToManyField(InferenceDetectionClassificationTracker, blank=True)
    inference_ocr = models.ManyToManyField(InferenceOCR, blank=True)
    # Key Inferences
    key_inference_classification = models.ManyToManyField(KeyInferenceClassification)
    key_inference_detection_classification = models.ManyToManyField(KeyInferenceDetectionClassification)
    key_inference_detection_classification_tracker = models.ManyToManyField(KeyInferenceDetectionClassificationTracker)
    key_inference_ocr = models.ManyToManyField(KeyInferenceOCR)
    def __str__(self):
        return f"{self.event_type.name} at {self.added_date} from {self.cameras}"





