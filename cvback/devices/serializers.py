from rest_framework import serializers
from .models import Camera, Area, InferenceComputer


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'


class InferenceComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceComputer
        fields = '__all__'
