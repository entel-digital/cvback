from django.db import models
from django_jsonform.models.fields import ArrayField
from cvback.devices.models import Camera, InferenceComputer
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator, FileExtensionValidator, RegexValidator


# TODO: Quizás hacer una nueva aplicación tipo "inferences" para simplificar el archivo ?


def validate_relative(value):
    if value < 0 or value > 1:
        raise ValidationError(
            _("%(value)s not between 0 and 1. We use relative areas of interest"),
            params={"value": value},
        )


# https://en.wikipedia.org/wiki/Software_versioning#Semantic_versioning
validate_semantic_versioning = RegexValidator('^\d{1,2}\.\d{1,2}\.\d{1,3}$')


class AreaOfInterest(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
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
    added_date = models.DateTimeField("date created", default=timezone.now)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    geometry = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    description = models.TextField(null=True, blank=True)


class Algorithm(models.Model):
    ALGORITHM_CHOICES = [
        ('detection_classification', 'Detection + classification model'),
        ('detection_classification_tracking', 'Detection + classification + tracking model'),
        ('classification', 'Classification model'),
        ('cl_classification', 'Classification classic computer vision'),
        ('business_logic', 'Custom business logic')
    ]

    kind = models.CharField(max_length=255, choices=ALGORITHM_CHOICES)
    added_date = models.DateTimeField("date created", default=timezone.now)
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=30, validators=[validate_semantic_versioning])
    repository = models.CharField(max_length=30, validators=[URLValidator])


class Label(models.Model):
    COLOR_GROUP_CHOICES = [
        ('person', 'Person'),
        ('animal', 'Animal'),
        ('vehicle', 'Vehicle'),
        ('id', 'Id'),
        ('ppe', 'PPE'),
        ('other', 'Other')
    ]

    name = models.CharField(max_length=255, unique=True)
    color_group = models.CharField(max_length=255, choices=COLOR_GROUP_CHOICES)

    def __str__(self):
        return self.name


class Frame(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    informed_date = models.DateTimeField("date informed", default=timezone.now)
    image = models.FileField(null=True, blank=True)
    cameras = models.ManyToManyField(Camera)


class KeyFrame(models.Model):
    name = models.CharField()
    frames = models.ManyToManyField(Frame)


class Video(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    informed_date = models.DateTimeField("date informed", default=timezone.now)
    video = models.FileField(null=True, blank=True)
    cameras = models.ManyToManyField(Camera)


class KeyVideo(models.Model):
    name = models.CharField()
    frames = models.ManyToManyField(Video)


class Inference(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    informed_date = models.DateTimeField("date informed", default=timezone.now)
    inference_computer = models.ForeignKey(InferenceComputer, on_delete=models.DO_NOTHING)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE, null=True, blank=True)
    confidence = models.FloatField(validators=[validate_relative])
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, null=True, related_name="%(class)s_inferences")

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date}"


class BoundingBox(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    informed_date = models.DateTimeField("date informed", default=timezone.now)
    top_left = ArrayField(models.FloatField(validators=[validate_relative]), size=2)
    bottom_right = ArrayField(models.FloatField(validators=[validate_relative]), size=2)

    class Meta:
        verbose_name_plural = "Bounding boxes"


class InferenceOCR(Inference):
    name = models.CharField(max_length=255)
    value = models.TextField()
    confidence = models.FloatField(validators=[validate_relative])


class KeyInferenceOCR(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceOCR, on_delete=models.CASCADE)


class InferenceDetectionClassification(Inference):
    bounding_boxes = models.ManyToManyField(BoundingBox)
    labels = models.ManyToManyField(Label)
    #frame = models.ForeignKey(Frame, on_delete=models.CASCADE, related_name='detections', null=True)

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
                raise ValidationError("The number of bounding boxes must match the number of labels")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.clean()


class KeyInferenceDetectionClassificationTracker(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceDetectionClassificationTracker, on_delete=models.CASCADE)


class InferenceClassification(Inference):
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.inference_computer} > {self.added_date} > {self.label}"


class KeyInferenceClassification(models.Model):
    name = models.CharField(max_length=255)
    inferences = models.ForeignKey(InferenceClassification, on_delete=models.CASCADE)


class EventType(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    name = models.CharField(max_length=30)
    version = models.CharField(max_length=30, validators=[validate_semantic_versioning])
    documentation = models.FileField(null=True,
                                     blank=True,
                                     validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return f"{self.name} {self.version}"


class Event(models.Model):
    added_date = models.DateTimeField("date created", default=timezone.now)
    informed_date = models.DateTimeField("date informed", default=timezone.now)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE)
    event_label = models.ForeignKey(Label,on_delete=models.CASCADE )
    cameras = models.ManyToManyField(Camera)
    frames = models.ManyToManyField(Frame)
    key_frames = models.ManyToManyField(KeyFrame)
    videos = models.ManyToManyField(Video, blank=True)
    key_videos = models.ManyToManyField(KeyVideo, blank=True)
    confidence = models.FloatField(validators=[validate_relative], default=0)
    labels_detected = models.ManyToManyField(Label, related_name='events_detected',blank=True)
    labels_missing = models.ManyToManyField(Label, related_name='events_missing',blank=True)

    # Inferences
    inference_classification = models.ManyToManyField(InferenceClassification, blank=True)
    inference_detection_classification = models.ManyToManyField(InferenceDetectionClassification, blank=True)
    inference_detection_classification_tracker = models.ManyToManyField(InferenceDetectionClassificationTracker,
                                                                        blank=True)
    inference_ocr = models.ManyToManyField(InferenceOCR, blank=True)
    # Key Inferences
    key_inference_classification = models.ManyToManyField(KeyInferenceClassification, blank=True)
    key_inference_detection_classification = models.ManyToManyField(KeyInferenceDetectionClassification, blank=True)
    key_inference_detection_classification_tracker = models.ManyToManyField(KeyInferenceDetectionClassificationTracker, blank=True)
    key_inference_ocr = models.ManyToManyField(KeyInferenceOCR, blank=True)

    def __str__(self):
        return f"{self.event_type.name} at {self.added_date} from {self.cameras}"

