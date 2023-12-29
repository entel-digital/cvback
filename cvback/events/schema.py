import graphene
from graphene_django import DjangoObjectType
from cvback.events.models import AreaOfInterest, BoundingBox, Inference, Event, Alert

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

class AlertType(DjangoObjectType):
    class Meta:
        model = Alert
        fields = "__all__"
