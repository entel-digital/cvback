import graphene
from graphene_django import DjangoObjectType
from cvback.events.models import (AreaOfInterest, LineOfInterest, Algorithm, Label, Frame, Video,
                                  KeyFrame, KeyVideo, BoundingBox, Inference, InferenceOCR, KeyInferenceOCR,
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
        fields = ("id", "image", "image_url")

    image_url = graphene.String()

    def resolve_image_url(self, info):
        return self.get_image_url()



class KeyFrameType(DjangoObjectType):
    class Meta:
        model = KeyFrame
        fields = ('id', 'name', 'frames')


class VideoType(DjangoObjectType):
    class Meta:
        model = Video
        fields = "__all__"


class KeyVideoType(DjangoObjectType):
    class Meta:
        model = KeyVideo
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
        fields = ("__all__")


class LabelType(DjangoObjectType):
    class Meta:
        model = Label
        fields = ("__all__")


class BoundingBoxType(DjangoObjectType):
    class Meta:
        model = BoundingBox
        fields = ("__all__")


class EventType(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = Event
        fields = ("__all__")
        filter_fields = {
            'id': ['exact', 'range', 'in', 'gte', 'lt'],
            'informed_date': ['gte', 'lt', 'exact']
        }
        interfaces = (graphene.relay.Node,)


class EventFilterAndPaginationType(graphene.ObjectType):
    events = graphene.List(EventType)
    global_total_number = graphene.Int()
    offset = graphene.Int(default_value=0)
    rows_per_page = graphene.Int(default_value=10)
    filtered = graphene.Boolean()
    filtered_by = graphene.List(graphene.String)
    label_text_filter = graphene.String()
    query_total_number = graphene.Int()
    labels_summary = graphene.types.JSONString()
    types_summary = graphene.types.JSONString()
