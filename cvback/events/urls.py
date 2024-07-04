from django.urls import path
from . import views
from cvback.events.views import BoundingBoxApiView, FrameApiView, InferenceClassificationApiView, InferenceDetectionClassificationApiView, InferenceDetectionClassificationTrackerApiView, InferenceOCRApiView, EventApiView, VideoApiView
from graphene_django.views import GraphQLView
from cvback.schema import schema


urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('bounding_box/', BoundingBoxApiView.as_view(), name='events_bounding_box'),
    path('frames/', FrameApiView.as_view(), name='events_frames'),
    path('inference_classification/', InferenceClassificationApiView.as_view(), name='events_inference_classification'),
    path('inference_detection_classification/', InferenceDetectionClassificationApiView.as_view(), name='events_inference_detection_classification'),
    path('inference_detection_classification_tracker/', InferenceDetectionClassificationTrackerApiView.as_view(), name='events_inference_detection_classification_tracker'),
    path('inference_ocr/', InferenceOCRApiView.as_view(), name='events_inference_ocr'),
    path('main_event/', EventApiView.as_view(), name='events_event'),
    path('videos/', VideoApiView.as_view(), name='events_videos'),

]
