from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from cvback.events.tasks import create_alert
from cvback.events.serializers import (BoundingBoxSerializer, FrameSerializer, InferenceClassificationSerializer,
                                       InferenceDetectionClassificationSerializer, VideoSerializer,
                                       InferenceDetectionClassificationTrackerSerializer, InferenceOCRSerializer,
                                       EventSerializer, KeyFrameSerializer, LabelSerializer, KeyVideoSerializer,
                                       LineOfInterestSerializer)
from cvback.events.models import (Frame, Label, KeyFrame, BoundingBox, InferenceClassification,
                                  InferenceDetectionClassification, InferenceDetectionClassificationTracker,
                                  InferenceOCR, Event, Video, KeyVideo, LineOfInterest)
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework_api_key.permissions import HasAPIKey

# TODO: filter by camera

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class BaseListCreateAPIView(ListCreateAPIView):
    permission_classes = [HasAPIKey]

    @classmethod
    def __init__(self, *args, **kwargs):
        self.queryset = self.model.objects.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoundingBoxApiView(BaseListCreateAPIView):
    model = BoundingBox
    serializer_class = BoundingBoxSerializer


class FrameApiView(BaseListCreateAPIView):
    model = Frame
    serializer_class = FrameSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        image = self.request.FILES.get('image')
        image_with_boundingboxes = self.request.FILES.get('image_with_boundingboxes')
        serializer.save(image=image, image_with_boundingboxes=image_with_boundingboxes)


class KeyFrameApiView(BaseListCreateAPIView):
    model = KeyFrame
    serializer_class = KeyFrameSerializer


class InferenceClassificationApiView(BaseListCreateAPIView):
    model = InferenceClassification
    serializer_class = InferenceClassificationSerializer


class InferenceDetectionClassificationApiView(BaseListCreateAPIView):
    model = InferenceDetectionClassification
    serializer_class = InferenceDetectionClassificationSerializer


class InferenceDetectionClassificationTrackerApiView(BaseListCreateAPIView):
    model = InferenceDetectionClassificationTracker
    serializer_class = InferenceDetectionClassificationTrackerSerializer


class InferenceOCRApiView(BaseListCreateAPIView):
    model = InferenceOCR
    serializer_class = InferenceOCRSerializer


class LabelApiView(BaseListCreateAPIView):
    model = Label
    serializer_class = LabelSerializer


class LineOfInterestApiView(BaseListCreateAPIView):
    model = LineOfInterest
    serializer_class = LineOfInterestSerializer

    def list(self, request, *args, **kwargs):
        instance = self.model.objects.filter(enabled=True).order_by('-added_modified').first()
        if instance:
            return Response({'line_position': instance.geometry[0]})
        return Response({'error': 'No line of interest found'}, status=status.HTTP_404_NOT_FOUND)


class EventApiView(ListCreateAPIView):
    model = Event
    serializer_class = EventSerializer
    permission_classes = [HasAPIKey]

    @classmethod
    def __init__(self, *args, **kwargs):
        self.queryset = self.model.objects.all()

    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            create_alert(Event.objects.get(id=serializer.data["id"]))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoApiView(BaseListCreateAPIView):
    model = Video
    serializer_class = VideoSerializer


class KeyVideoApiView(BaseListCreateAPIView):
    model = KeyVideo
    serializer_class = KeyVideoSerializer
