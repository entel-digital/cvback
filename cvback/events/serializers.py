from rest_framework import serializers
from cvback.events.models import BoundingBox, Frame, Video, InferenceDetectionClassificationTracker, InferenceDetectionClassification, InferenceOCR, Event
#from drf_compound_fields.fields import ListField
from cvback.events.models import AreaOfInterest, Event, InferenceDetectionClassification, InferenceClassification, Label

# TODO: +Frames, +Videos, +Inference classification, +Inference detection classification tracker, +Inference detection classification, +Inference ocr, +Event
class BoundingBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = "__all__"

class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"

class InferenceClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceClassification
        fields = "__all__"

class InferenceDetectionClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceDetectionClassification
        fields = "__all__"

class InferenceDetectionClassificationTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceDetectionClassificationTracker
        fields = "__all__"

class InferenceOCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceOCR
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


