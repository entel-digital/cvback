from django.core.management.base import BaseCommand
from cvback.devices.models import Area, Camera, InferenceComputer
from cvback.events.models import (
    AreaOfInterest, LineOfInterest, Algorithm, Label, Frame, KeyFrame, Video, KeyVideo,
    BoundingBox, InferenceOCR, KeyInferenceOCR, InferenceDetectionClassification,
    KeyInferenceDetectionClassification, InferenceDetectionClassificationTracker,
    KeyInferenceDetectionClassificationTracker, InferenceClassification,
    KeyInferenceClassification, EventType, Event
)

class Command(BaseCommand):
    help = 'Deletes all fake data'

    def handle(self, *args, **options):
        # Delete in reverse order of dependencies
        self.stdout.write('Deleting fake data...')

        Event.objects.all().delete()
        EventType.objects.all().delete()

        KeyInferenceClassification.objects.all().delete()
        KeyInferenceDetectionClassificationTracker.objects.all().delete()
        KeyInferenceDetectionClassification.objects.all().delete()
        KeyInferenceOCR.objects.all().delete()

        InferenceClassification.objects.all().delete()
        InferenceDetectionClassificationTracker.objects.all().delete()
        InferenceDetectionClassification.objects.all().delete()
        InferenceOCR.objects.all().delete()

        BoundingBox.objects.all().delete()

        KeyVideo.objects.all().delete()
        Video.objects.all().delete()
        KeyFrame.objects.all().delete()
        Frame.objects.all().delete()

        Label.objects.all().delete()
        Algorithm.objects.all().delete()
        LineOfInterest.objects.all().delete()
        AreaOfInterest.objects.all().delete()

        InferenceComputer.objects.all().delete()
        Camera.objects.all().delete()
        Area.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully deleted all fake data'))
