from rest_framework import serializers
from cvback.events.models import BoundingBox, Frame, Video, InferenceDetectionClassificationTracker, InferenceDetectionClassification, InferenceOCR, Event
#from drf_compound_fields.fields import ListField
from cvback.events.models import AreaOfInterest, Event, InferenceDetectionClassification, InferenceClassification, Label, KeyVideos, KeyInferenceClassification, KeyInferenceDetectionClassification, KeyInferenceDetectionClassificationTracker, KeyInferenceOCR, KeyFrames
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

class KeyVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyVideos
        fields = "__all__"

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ("id",)


class KeyFramesSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyFrames
        fields = "__all__"

class EventSerializer(serializers.ModelSerializer):

    cameras = CameraSerializer(many=True,read_only=True )

    
    labels_detected = LabelSerializer(required=False, many=True, read_only=True)
    labels_missing = LabelSerializer(required=False, many=True,read_only=True)
    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        
        event = Event.objects.create(event_type=validated_data["event_type"],
                                     event_label=validated_data["event_label"],
                                     inference_detection_classification=validated_data["inference_detection_classification"]
                                     )
        [event.frames.add(frame.id) for frame in validated_data["frames"]]
        [event.key_frames.add(frame.id) for frame in validated_data['key_frames']]
                
        [event.inference_classification.add(inference.id) for inference in validated_data["inference_classification"]]
        
        [event.inference_detection_classification_tracker.add(inference.id) for inference in validated_data["inference_detection_classification_tracker"]]
        [event.inference_ocr.add(inference.id) for inference in validated_data["inference_ocr"]]
        print(validated_data.keys())
        
        return event

