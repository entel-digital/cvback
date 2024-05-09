from django.core.management.base import BaseCommand
from cvback.devices.models import Area, Camera, InferenceComputer
from cvback.events.models import AreaOfInterest, BoundingBox, Inference, \
    InferenceDetectionClassification, InferenceClassification, Label, Event, Alert

class Command(BaseCommand):
    help = 'Deletes fake data from the database'

    def handle(self, *args, **options):
        Alert.objects.all().delete()
        InferenceDetectionClassification.objects.all().delete()
        InferenceClassification.objects.all().delete()
        Label.objects.all().delete()
        Camera.objects.all().delete()
        InferenceComputer.objects.all().delete()
        AreaOfInterest.objects.all().delete()
        BoundingBox.objects.all().delete()
        Event.objects.all().delete()


        self.stdout.write(self.style.SUCCESS('Successfully deleted fake data'))