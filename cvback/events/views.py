from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from cvback.events.serializers import BoundingBoxSerializer, FrameSerializer, InferenceClassificationSerializer, InferenceDetectionClassificationSerializer, InferenceDetectionClassificationTrackerSerializer, InferenceOCRSerializer, VideoSerializer, EventSerializer
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import logging
# Create your views here.
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
class FrameApiView(APIView):
    def post(self, request, format=None):
        serializer = FrameSerializer(data=request.data)
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