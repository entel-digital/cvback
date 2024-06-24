import graphene
from graphene_django import DjangoObjectType
from cvback.events.models import (AreaOfInterest, LineOfInterest, Algorithm, Label, Frame, Video,
                                  KeyFrames, KeyVideos, BoundingBox, Inference, InferenceOCR, KeyInferenceOCR,
                                  InferenceDetectionClassification, KeyInferenceDetectionClassification,
                                  InferenceClassification, KeyInferenceClassification,
                                  InferenceDetectionClassificationTracker, KeyInferenceDetectionClassificationTracker,
                                  EventType, Event)

class AreaOfInterestType(DjangoObjectType):
    class Meta:
        model = AreaOfInterest
        fields = "__all__"

class LineOfInterestType(DjangoObjectType):
    class Meta:
        model = LineOfInterest
        fields = "__all__"

class AlgorithmType(DjangoObjectType):
    class Meta:
        model = Algorithm
        fields = "__all__"

class FrameType(DjangoObjectType):
    class Meta:
        model = Frame
        fields = "__all__"

class KeyFramesType(DjangoObjectType):
    class Meta:
        model = KeyFrames
        fields = ('id', 'name', 'frames')
class VideoType(DjangoObjectType):
    class Meta:
        model = Video
        fields = "__all__"

class KeyVideosType(DjangoObjectType):
    class Meta:
        model = KeyVideos
        fields = "__all__"

class InferenceType(DjangoObjectType):
    class Meta:
        model = Inference
        fields = "__all__"

class InferenceOCRType(DjangoObjectType):
    class Meta:
        model = InferenceOCR
        fields = "__all__"

class KeyInferenceOCRType(DjangoObjectType):
    class Meta:
        model = KeyInferenceOCR
        fields = "__all__"

class InferenceOCRType(DjangoObjectType):
    class Meta:
        model = InferenceOCR
        fields = "__all__"

class InferenceDetectionClassificationType(DjangoObjectType):
    class Meta:
        model = InferenceDetectionClassification
        fields = "__all__"

class KeyInferenceDetectionClassificationType(DjangoObjectType):
    class Meta:
        model = KeyInferenceDetectionClassification
        fields = "__all__"

class InferenceClassificationType(DjangoObjectType):
    class Meta:
        model = InferenceClassification
        fields = "__all__"

class KeyInferenceClassificationType(DjangoObjectType):
    class Meta:
        model = KeyInferenceClassification
        fields = "__all__"

class InferenceDetectionClassificationTrackerType(DjangoObjectType):
    class Meta:
        model = InferenceDetectionClassificationTracker
        fields = "__all__"

class KeyInferenceDetectionClassificationTrackerType(DjangoObjectType):
    class Meta:
        model = KeyInferenceDetectionClassificationTracker
        fields = "__all__"


class EventTypeType(DjangoObjectType):
    class Meta:
        model = EventType
        fields = ('id', 'name', 'added_date')

class LabelType(DjangoObjectType):
    class Meta:
        model = Label
        fields = ('id', 'name', 'color_group')

class BoundingBoxType(DjangoObjectType):
    class Meta:
        model = BoundingBox
        fields = ('id', 'top_left', 'bottom_right')

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = (
            'id', 'added_date', 'event_type', 'labels', 'bounding_boxes', 'keyframes',
            'labels_detected', 'labels_missing'
        )
