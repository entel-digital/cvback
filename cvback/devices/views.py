from django.http import HttpResponse
from rest_framework import viewsets
from cvback.devices.models import Area, Camera, InferenceComputer
from cvback.devices.serializers import AreaSerializer, CameraSerializer, InferenceComputerSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the devices index.")


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer


class InferenceComputerViewSet(viewsets.ModelViewSet):
    queryset = InferenceComputer.objects.all()
    serializer_class = InferenceComputerSerializer
