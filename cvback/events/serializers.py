from rest_framework import serializers
from cvback.events.models import BoundingBox, Frame, Video, InferenceDetectionClassificationTracker, InferenceDetectionClassification, InferenceOCR, Event
#from drf_compound_fields.fields import ListField
from cvback.events.models import AreaOfInterest, Event, InferenceDetectionClassification, InferenceClassification, Label, KeyVideo, KeyInferenceClassification, KeyInferenceDetectionClassification, KeyInferenceDetectionClassificationTracker, KeyInferenceOCR, KeyFrame
from cvback.devices.serializers import CameraSerializer
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

class KeyInferenceClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyInferenceClassification
        fields = "__all__"

class InferenceDetectionClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceDetectionClassification
        fields = "__all__"

class KeyInferenceDetectionClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyInferenceDetectionClassification
        fields = "__all__"

class InferenceDetectionClassificationTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceDetectionClassificationTracker
        fields = "__all__"

class KeyInferenceDetectionClassificationTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyInferenceDetectionClassificationTracker
        fields = "__all__"

class InferenceOCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceOCR
        fields = "__all__"

class KeyInferenceOCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyInferenceOCR
        fields = "__all__"

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

class KeyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVideo
        fields = "__all__"

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ("id",)

class KeyFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyFrame
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

