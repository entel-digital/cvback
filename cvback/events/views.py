import csv
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str
from django.core.exceptions import FieldDoesNotExist
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
from csv_export.views import CSVExportView
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


class CustomCSVExportView(CSVExportView):
    specify_separator = False
    permission_classes = []
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("403 Forbidden",status=403)
        id_equals_to = request.GET.get('id_equals_to')
        date_equals_to = request.GET.get('date_equals_to')
        date_lower_than = request.GET.get('date_lower_than')
        date_greater_than_equal = request.GET.get('date_greater_than_equal')
        label_text_filter = request.GET.get('label_text_filter')

        qs = Event.objects.all()
        if label_text_filter:
            qs = qs.filter(event_label__name__icontains=label_text_filter)
        if id_equals_to:
            qs = qs.filter(id=id_equals_to)
        if date_equals_to:
            qs = qs.filter(informed_date=date_equals_to)
        if date_lower_than:
            qs = qs.filter(informed_date__lt=date_lower_than)
        if date_greater_than_equal:
            qs = qs.filter(informed_date__gte=date_greater_than_equal)

        field_names = self.get_fields(qs)

        response = HttpResponse(content_type="text/csv")

        filename = self.get_filename(qs)
        if not filename.endswith(".csv"):
            filename += ".csv"
        response["Content-Disposition"] = 'attachment; filename="{}"'.format(filename)

        writer = csv.writer(response, **self.get_csv_writer_fmtparams())

        if self.specify_separator:
            response.write("sep={}{}".format(writer.dialect.delimiter, writer.dialect.lineterminator))

        if self.header:
            writer.writerow([self.get_header_name(qs.model, field_name) for field_name in list(field_names)])

        for obj in qs:
            writer.writerow([self.get_field_value(obj, field) for field in field_names])

        return response


    def get_header_name(self, model, field_name):
        """Override if a custom value or behaviour is required for specific fields."""
        "FIELDNAME"
        return field_name

    def get_field_value(self, obj, field_name):
        """Override if a custom value or behaviour is required for specific fields."""
        if "__" not in field_name:
            if hasattr(obj, "all") and hasattr(obj, "iterator"):
                return ",".join([force_str(getattr(ro, field_name)) for ro in obj.all()])

            try:
                field = obj._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(obj, field_name):
                    raise e
                # field_name is a property.
                return getattr(obj, field_name)

            if field.many_to_one:
                return str(getattr(obj, field_name))

            value = field.value_from_object(obj)
            if field.many_to_many:
                return ",".join([force_str(ro) for ro in value])
            elif field.choices:
                if value is None or force_str(value).strip() == "":
                    return ""
                return dict(field.choices)[value]
            return value
        else:
            related_field_names = field_name.split("__")
            if obj.__class__.__name__ == 'ManyRelatedManager':
                objs = []
                for sobj in obj.all():
                    related_obj = getattr(sobj, related_field_names[0])
                    related_field_name = "__".join(related_field_names[1:])
                    objs.append(self.get_field_value(related_obj, related_field_name))
                return ", ".join([force_str(o) for o in objs])
            else:    
                related_obj = getattr(obj, related_field_names[0])
                related_field_name = "__".join(related_field_names[1:])
            return self.get_field_value(related_obj, related_field_name)

class DataExportView(CustomCSVExportView):
    model = Event
    fields = (  'id',
                'added_date',
                'informed_date',
                'confidence',
                'event_type__id',
                'event_type__added_date',
                'event_type__name',
                'event_type__version',
                'event_type__documentation',
                'event_label__id',
                'event_label__name',
                'event_label__color_group',
                'cameras',
                'cameras__added_date',
                'cameras__added_modified',
                'cameras__enabled',
                'cameras__name',
                'cameras__primary_stream',
                'cameras__location',
                'cameras__last_seen_online',
                'cameras__need_cleaning',
                'cameras__need_physical_maintenance',
                'cameras__need_replacement',
                'cameras__photo',
                'cameras',
                'cameras__area__id',
                'cameras__area__added_date',
                'cameras__area__added_modified',
                'cameras__area__name',
                'cameras__area__diagram',
                'frames__id',
                'frames__added_date',
                'frames__informed_date',
                'frames__image',
                'frames__cameras__id',
                'key_frames__id',
                'key_frames__name',
                'key_frames__frames__id',
                'videos__id',
                'videos__added_date',
                'videos__informed_date',
                'videos__video',
                'videos__cameras__id',
                'key_videos__id',
                'key_videos__name',
                'key_videos__videos__id',
                'labels_detected__id',
                'labels_detected__name',
                'labels_detected__color_group',
                'labels_missing__name',
                'labels_missing__color_group',
                'inference_classification__id',
                'inference_classification__added_date',
                'inference_classification__informed_date',
                'inference_classification__confidence',
                'inference_classification__inference_computer__id',
                'inference_classification__inference_computer__added_date',
                'inference_classification__inference_computer__added_modified',
                'inference_classification__inference_computer__enabled',
                'inference_classification__inference_computer__name',
                'inference_classification__inference_computer__location',
                'inference_classification__algorithm__id',
                'inference_classification__algorithm__kind',
                'inference_classification__algorithm__added_date',
                'inference_classification__algorithm__name',
                'inference_classification__algorithm__version',
                'inference_classification__algorithm__repository',
                'inference_classification__frame__id',
                'inference_classification__label__id',
                'inference_classification__label__name',
                'inference_classification__label__color_group',
                'inference_detection_classification',
                'inference_detection_classification_tracker',
                'inference_ocr',
                'key_inference_classification',
                'key_inference_detection_classification',
                'key_inference_detection_classification_tracker',
                'key_inference_ocr'
                )

    def get_filename(self, queryset):
        return "data-export-{!s}.csv".format(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
