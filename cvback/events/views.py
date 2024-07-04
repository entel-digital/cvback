from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from cvback.events.serializers import BoundingBoxSerializer, FrameSerializer, InferenceClassificationSerializer, InferenceDetectionClassificationSerializer, InferenceDetectionClassificationTrackerSerializer, InferenceOCRSerializer, VideoSerializer, EventSerializer, KeyFramesSerializer
from cvback.events.models import Frame, Label, KeyFrames
from cvback.devices.serializers import CameraSerializer
from cvback.devices.models import Camera
from django.views import View
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging

# TODO: filter by camera

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class BoundingBoxApiView(APIView):
    def post(self, request, format=None):
        serializer = BoundingBoxSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class FrameApiView(ListCreateAPIView):
    model = Frame
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer
    
    def create(self, request, *args, **kwargs):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(csrf_exempt, name='dispatch')
class InferenceClassificationApiView(APIView):
    def post(self, request, format=None):
        serializer = InferenceClassificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@method_decorator(csrf_exempt, name='dispatch')
class InferenceDetectionClassificationApiView(APIView):
    def post(self, request, format=None):
        serializer = InferenceDetectionClassificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class InferenceDetectionClassificationTrackerApiView(APIView):
    def post(self, request, format=None):
        serializer = InferenceDetectionClassificationTrackerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class InferenceOCRApiView(APIView):
    def post(self, request, format=None):
        serializer = InferenceOCRSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class EventApiView(APIView):
    def post(self, request, format=None):
        
        
        label_dict = {label.name:label.id for label in Label.objects.all()}
        

        event_label= request.data.get("event_label")
        aux_detected = []
        for label in request.data["labels_detected"]:
            lid = label_dict.get(label,None)
            if not lid:
                lid=1
            aux_detected.append({"id":str(lid)})

        aux_missing = []
        for label in request.data["labels_missing"]:
            lid = label_dict.get(label,None)
            lid = label_dict.get(label,None)
            if not lid:
                lid=1
            aux_missing.append({"id":str(lid)})

        key_frames = []
        for frame_id in request.data["key_frames"]:

            new_key_frame = KeyFrames()
            new_key_frame.save()
            new_key_frame.frames.add(Frame.objects.get(id=frame_id))
            key_frames.append(new_key_frame.id)
        
        aux_cameras = []
        for camera in request.data["cameras"]:
            actual_camera = Camera.objects.get(id=camera)
            actual_camera = CameraSerializer(actual_camera).data
            actual_camera.update({"id":camera})
            aux_cameras.append(actual_camera)
        print(aux_cameras)

        request.data.update({"key_frames":key_frames,
                             "labels_detected":aux_detected,
                             "labels_missing":aux_missing,
                             "event_label":label_dict.get(event_label,1) if event_label else 1,
                             "cameras":aux_cameras
                               })
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class VideoApiView(APIView):
    def post(self, request, format=None):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)