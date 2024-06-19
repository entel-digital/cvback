import graphene
from cvback.events.schema import (AreaOfInterestType, LineOfInterestType, AlgorithmType, LabelType, 
                                  FrameType, VideoType, KeyFramesType, KeyVideosType, BoundingBoxType, 
                                  InferenceType, InferenceOCRType, KeyInferenceOCRType, InferenceOCRType, 
                                  InferenceDetectionClassificationType, KeyInferenceDetectionClassificationType, 
                                  InferenceClassificationType, KeyInferenceClassificationType, 
                                  InferenceDetectionClassificationTrackerType, 
                                  KeyInferenceDetectionClassificationTrackerType, EventType)
from cvback.events.models import (AreaOfInterest, LineOfInterest, Algorithm, Label, Frame, Video, KeyFrames, 
                                  KeyVideos,Inference, BoundingBox, InferenceOCR, KeyInferenceOCR,
                                  InferenceDetectionClassification, KeyInferenceDetectionClassification,
                                  InferenceDetectionClassificationTracker, KeyInferenceDetectionClassificationTracker,
                                  InferenceClassification, KeyInferenceClassification, Event)

class UpdateEventMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        tag = graphene.String()

    event = graphene.Field(EventType)

    def mutate(self, info, id, tag):
        event = Event.objects.get(pk=id)
        event.tag = tag
        event.save()
        return UpdateEventMutation(event=event)

class Query(graphene.ObjectType):
    all_area_of_interest = graphene.List(AreaOfInterestType)
    all_line_of_interest = graphene.List(LineOfInterestType)
    all_algorithms = graphene.List(AlgorithmType)
    all_labels = graphene.List(LabelType)
    all_frames = graphene.List(FrameType)
    all_videos = graphene.List(VideoType)
    all_key_frames = graphene.List(KeyFramesType)
    all_key_videos = graphene.List(KeyVideosType)
    all_bounding_boxes = graphene.List(BoundingBoxType)
    all_inference_ocr = graphene.List(InferenceOCRType)
    all_key_inference_ocr = graphene.List(KeyInferenceOCRType)
    all_inference_detection_classification = graphene.List(InferenceDetectionClassificationType)
    all_key_inference_detection_classification = graphene.List(KeyInferenceDetectionClassificationType)
    all_inference_detection_classification_tracker = graphene.List(InferenceDetectionClassificationTrackerType)
    all_key_inference_detection_classification_tracker = graphene.List(KeyInferenceDetectionClassificationTrackerType)
    all_inference_classification = graphene.List(InferenceClassificationType)
    all_key_inference_classification = graphene.List(KeyInferenceClassificationType)
    all_events = graphene.List(EventType)

    def resolve_all_area_of_interest(self, info):
        return AreaOfInterest.objects.all()

    def resolve_all_line_of_interest(self, info):
        return LineOfInterest.objects.all()

    def resolve_all_algorithms(self, info):
        return Algorithm.objects.all()

    def resolve_all_labels(self, info):
        return Label.objects.all()

    def resolve_all_frames(self, info):
        return Frame.objects.all()

    def resolve_all_videos(self, info):
        return Video.objects.all()

    def resolve_all_key_frames(self, info):
        return KeyFrames.objects.all()

    def resolve_all_key_videos(self, info):
        return KeyVideos.objects.all()

    def resolve_all_bounding_boxes(self, info):
        return BoundingBox.objects.all()

    def resolve_all_inference_ocr(self, info):
        return InferenceOCR.objects.all()

    def resolve_all_key_inference_ocr(self, info):
        return KeyInferenceOCR.objects.all()

    def resolve_all_inference_detection_classification(self, info):
        return InferenceDetectionClassification.objects.all()

    def resolve_all_key_inference_detection_classification(self, info):
        return KeyInferenceDetectionClassification.objects.all()

    def resolve_all_inference_detection_classification_tracker(self, info):
        return InferenceDetectionClassificationTracker.objects.all()

    def resolve_all_key_inference_detection_classification_tracker(self, info):
        return KeyInferenceDetectionClassificationTracker.objects.all()

    def resolve_all_inference_classification(self, info):
        return InferenceClassification.objects.all()

    def resolve_all_key_inference_classification(self, info):
        return KeyInferenceClassification.objects.all()

    def resolve_all_events(self, info):
        return Event.objects.all()

class Mutation(graphene.ObjectType):
    update_event = UpdateEventMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
