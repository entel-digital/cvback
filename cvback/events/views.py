from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings
from cvback.events.tasks import create_alert, save_file
from cvback.events.serializers import (BoundingBoxSerializer, FrameSerializer, InferenceClassificationSerializer,
                                       InferenceDetectionClassificationSerializer, VideoSerializer,
                                       InferenceDetectionClassificationTrackerSerializer, InferenceOCRSerializer,
                                       EventSerializer, KeyFrameSerializer, LabelSerializer, KeyVideoSerializer,
                                       LineOfInterestSerializer, KeyInferenceClassificationSerializer)
from cvback.events.models import (Frame, Label, KeyFrame, BoundingBox, InferenceClassification,
                                  InferenceDetectionClassification, InferenceDetectionClassificationTracker,
                                  InferenceOCR, Event, Video, KeyVideo, LineOfInterest, KeyInferenceClassification)
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework_api_key.permissions import HasAPIKey
from datetime import datetime 
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
        serializer.save(image=image)


class KeyFrameApiView(BaseListCreateAPIView):
    model = KeyFrame
    serializer_class = KeyFrameSerializer


class InferenceClassificationApiView(BaseListCreateAPIView):
    model = InferenceClassification
    serializer_class = InferenceClassificationSerializer

class KeyInferenceClassificationApiView(BaseListCreateAPIView):
    model = KeyInferenceClassification
    serializer_class = KeyInferenceClassificationSerializer


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


class CustomCSVExportView(View):
    
    specify_separator = False
    permission_classes = []
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("403 Forbidden",status=403)
        
        id_equals_to = request.GET.get('id_equals_to')
        date_equals_to = request.GET.get('date_equals_to')
        date_lower_than = request.GET.get('date_lower_than')
        date_greater_than_equal = request.GET.get('date_greater_than_equal')
        label_id_filter = request.GET.get('label_id_filter')
        format = request.GET.get('format')
        full_data = request.GET.get('full_data',False)
        sorted_by = request.GET.get('sorted_by',None)
        asc = request.GET.get('asc')

        request_username = request.user.username
        request_email = request.user.email

        save_file.delay(request_username, request_email, full_data, format, id_equals_to, date_equals_to, date_lower_than, date_greater_than_equal, label_id_filter, sorted_by, asc)
        return HttpResponse("YOUR REQUEST IS BEING PROCESSED", status=200)