from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from cvback.events.models import Event
from cvback.events.serializers import EventSerializer
from django.views import View
import json
import logging
# Create your views here.
# TODO: filter by camera

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class MQTTEventView(View):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode('utf-8'))
            serializer = EventSerializer(data=payload)
            
            if serializer.is_valid():
                event = Event.object.create(
                    event_type_id=serializer.validated_data['event_type_id'],
                    confidence=serializer.validated_data.get('confidence')
                )
                
                camera_ids = serializer.validated_data.get('camera_ids', [])
                event.cameras.add(*Camera.objects.filter(id__in=camera_ids))
                
                event.labels_detected.add(*serializer.validated_data.get('labels_detected', []))
                event.labels_missing.add(*serializer.validated_data.get('labels_missing', []))
                
                event.key_inference_classification.add(*serializer.validated_data.get('key_inference_classification_ids', []))
                event.key_inference_detection_classification.add(*serializer.validated_data.get('key_inference_detection_classification_ids', []))
                event.key_inference_detection_classification_tracker.add(*serializer.validated_data.get('key_inference_detection_classification_tracker_ids', []))
                event.key_inference_ocr.add(*serializer.validated_data.get('key_inference_ocr_ids', []))
                
                event.save()
                
                return JsonResponse({'status': 'success', 'event_id': event.id}, status=201)
            else:
                return JsonResponse({'status': 'error', 'errors': serializer.errors}, status=400)

        except json.JSONDecodeError as json_error:
            logger.error(f"JSON Decode Error: {json_error}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)