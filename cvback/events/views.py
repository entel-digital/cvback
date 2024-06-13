from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from cvback.events.models import AreaOfInterest, Event
from cvback.events.serializers import EventSerializer, AreaOfInterestSerializer
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

            data = {
                'camera_id': payload.get('camera_id'),
                'inference_detection_classification_id': payload.get('inference_detection_classification_id'),
                'inference_classification_id': payload.get('inference_classification_id'),
            }

            event = Event.objects.create(
                camera_id=data['camera_id'],
                inference_detection_classification_id=data.get('inference_detection_classification_id'),
                inference_classification_id=data.get('inference_classification_id'),
            )
            
            return JsonResponse({'status': 'success', 'event_id': event.id}, status=201)

        except json.JSONDecodeError as json_error:
            logger.error(f"JSON Decode Error: {json_error}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON payload'}, status=400)

        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
@csrf_exempt
def areas_of_interest_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        areas_of_interest = AreaOfInterest.objects.all()
        serializer = AreaOfInterestSerializer(areas_of_interest, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AreaOfInterestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def area_of_interest_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        area_of_interest = AreaOfInterest.objects.get(pk=pk)
    except AreaOfInterest.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = AreaOfInterestSerializer(area_of_interest)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AreaOfInterestSerializer(area_of_interest, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        area_of_interest.delete()
        return HttpResponse(status=204)
