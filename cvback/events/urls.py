from django.urls import path
from . import views
from cvback.events.views import BoundingBoxApiView, FrameApiView, InferenceClassificationApiView, InferenceDetectionClassificationApiView, InferenceDetectionClassificationTrackerApiView, InferenceOCRApiView, EventApiView, VideoApiView
from graphene_django.views import GraphQLView
from cvback.schema import schema


urlpatterns = [
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('rest/bounding_box/', BoundingBoxApiView.as_view(), name='events_bounding_box'),
    path('rest/frame/', FrameApiView.as_view(), name='events_frame'),
    path('rest/inference_classification/', InferenceClassificationApiView.as_view(), name='events_inference_classification'),
    path('rest/inference_detection_classification/', InferenceDetectionClassificationApiView.as_view(), name='events_inference_detection_classification'),
    path('rest/inference_detection_classification_tracker/', InferenceDetectionClassificationTrackerApiView.as_view(), name='events_inference_detection_classification_tracker'),
    path('rest/inference_ocr/', InferenceOCRApiView.as_view(), name='events_inference_ocr'),
    path('rest/event/', EventApiView.as_view(), name='events_event'),
    path('rest/video/', VideoApiView.as_view(), name='events_video'),

]
