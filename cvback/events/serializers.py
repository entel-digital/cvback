from rest_framework import serializers
from cvback.events.models import BoundingBox
#from drf_compound_fields.fields import ListField
from cvback.events.models import AreaOfInterest, Event, InferenceDetectionClassification, InferenceClassification, Label
#
# class EventSerializer(serializers.Serializer):
#     event_type_id = serializers.PrimaryKeyRelatedField(queryset=EventType.objects.all())
#     camera_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
#     confidence = serializers.FloatField(required=False)
#     labels_detected = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all(), required=False)
#     labels_missing = serializers.PrimaryKeyRelatedField(many=True, queryset=Label.objects.all(), required=False)
#     #Agregar boundingboxes
#     key_inference_classification_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyInferenceClassification.objects.all(), required=False)
#     key_inference_detection_classification_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyInferenceDetectionClassification.objects.all(), required=False)
#     key_inference_detection_classification_tracker_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyInferenceDetectionClassificationTracker.objects.all(), required=False)
#     key_inference_ocr_ids = serializers.PrimaryKeyRelatedField(many=True, queryset=KeyInferenceOCR.objects.all(), required=False)
#
#     def validate_confidence(self, value):
#         if value is not None and (value < 0 or value > 1):
#             raise serializers.ValidationError("Confidence must be between 0 and 1")
#         return value
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Event.objects.create(**validated_data)
#
#

# TODO: +Frames, +Videos, +Inference classification, +Inference detection classification tracker, +Inference detection classification, +Inference ocr, +Event
class BoundingBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundingBox
        fields = "__all__"
