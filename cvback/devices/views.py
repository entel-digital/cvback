from django.http import HttpResponse
from rest_framework import viewsets
from cvback.devices.models import Camera, InferenceComputer
from cvback.devices.serializers import CameraSerializer, InferenceComputerSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the devices index.")


class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

class InferenceComputerViewSet(viewsets.ModelViewSet):
    queryset = InferenceComputer.objects.all()
    serializer_class = InferenceComputerSerializer