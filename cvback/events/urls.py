from django.urls import path
from django.conf import settings
from cvback.events.views import (BoundingBoxApiView, FrameApiView, InferenceClassificationApiView,
                                 InferenceDetectionClassificationApiView, EventApiView,
                                 InferenceDetectionClassificationTrackerApiView, InferenceOCRApiView,
                                 VideoApiView, KeyFrameApiView, LabelApiView, KeyVideoApiView,
                                 LineOfInterestApiView, CustomCSVExportView, LoginByLinkView,
                                 AuthenticatedGraphQlView)

from cvback.schema import schema
# from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('graphql/', AuthenticatedGraphQlView.as_view(graphiql=settings.GRAPHIQL_GRAPHIC_INTERFACE, schema=schema)),
    path('labels/', LabelApiView.as_view(), name="events_label"),
    path('bounding_box/', BoundingBoxApiView.as_view(), name='events_bounding_box'),
    path('frames/', FrameApiView.as_view(), name='events_frames'),
    path('key_frames/', KeyFrameApiView.as_view(), name='events_key_frames'),
    path('inference_classification/', InferenceClassificationApiView.as_view(),
         name='events_inference_classification'),
    path('inference_detection_classification/', InferenceDetectionClassificationApiView.as_view(),
         name='events_inference_detection_classification'),
    path('inference_detection_classification_tracker/', InferenceDetectionClassificationTrackerApiView.as_view(),
         name='events_inference_detection_classification_tracker'),
    path('inference_ocr/', InferenceOCRApiView.as_view(), name='events_inference_ocr'),
    path('main_event/', EventApiView.as_view(), name='events_event'),
    path('videos/', VideoApiView.as_view(), name='events_videos'),
    path('key_videos/', KeyVideoApiView.as_view(), name='events_key_videos'),
    path('line_of_interest/', LineOfInterestApiView.as_view(), name='events_line_of_interest'),
    path('csv_events/', CustomCSVExportView.as_view(), name = 'events_csv2'),
    path('login_by_link/', LoginByLinkView.as_view(), name='events_login_by_link'),
]
     