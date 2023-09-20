from rest_framework import serializers
#from drf_compound_fields.fields import ListField
from .models import AreaOfInterest


class AreaOfInterestSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    added_date = serializers.DateTimeField(read_only=True)
    added_modified = serializers.DateTimeField(read_only=True)
    enabled = serializers.BooleanField()
    name = serializers.CharField(max_length=255)
    camera = serializers.SlugRelatedField(slug_field='name', read_only=True)
    geometry = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField(), allow_empty=False, min_length=2, max_length=2
            )
        )
    # geometry = ListField(ListField(serializers.FloatField(), allow_empty=False, min_length=2, max_length=2))

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return AreaOfInterest.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.enabled = validated_data.get('enabled', instance.enabled)
        instance.name = validated_data.get('name', instance.name)
        instance.camera = validated_data.get('camera', instance.camera)
        instance.geometry = validated_data.get('geometry', instance.geometry)
        instance.save()
        return instance
