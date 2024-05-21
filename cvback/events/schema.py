from graphene_django import DjangoObjectType
from cvback.events.models import AreaOfInterest, BoundingBox, Inference, InferenceDetectionClassification, InferenceClassification, Event

class AreaOfInterestType(DjangoObjectType):
    class Meta:
        model = AreaOfInterest
        fields = "__all__"

class BoundingBoxType(DjangoObjectType):
    class Meta:
        model = BoundingBox
        fields = "__all__"

class InferenceType(DjangoObjectType):
    class Meta:
        model = Inference
        fields = "__all__"

class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"

class InferenceDetectionClassificationType(DjangoObjectType):
    class Meta:
        model = InferenceDetectionClassification
        fields = "__all__"

class InferenceClassificationType(DjangoObjectType):
    class Meta:
        model = InferenceClassification
        fields = "__all__"
