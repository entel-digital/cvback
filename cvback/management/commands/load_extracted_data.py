import json
from django.core.management.base import BaseCommand
from cvback.devices.models import Camera, InferenceComputer, Area
from cvback.events.models import Label, EventType, BoundingBox, Algorithm

class Command(BaseCommand):
    help = 'Load data from extracted_data.json into the database'

    def handle(self, *args, **options):
        with open('cvback/management/commands/extracted_data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create Areas
        for area_data in data['areas']:
            Area.objects.get_or_create(id=area_data['id'], defaults=area_data)
        self.stdout.write(self.style.SUCCESS(f"Created {len(data['areas'])} areas"))

        # Create Cameras
        for camera_data in data['cameras']:
            Camera.objects.get_or_create(id=camera_data['id'], defaults=camera_data)
        self.stdout.write(self.style.SUCCESS(f"Created {len(data['cameras'])} cameras"))

        # Create Inference Computers
        for ic_data in data['inference_computers']:
            InferenceComputer.objects.get_or_create(id=ic_data['id'], defaults=ic_data)
        self.stdout.write(self.style.SUCCESS(f"Created {len(data['inference_computers'])} inference computers"))

        # Create Labels
        for label_data in data['labels']:
            Label.objects.get_or_create(id=label_data['id'], defaults=label_data)
        self.stdout.write(self.style.SUCCESS(f"Created {len(data['labels'])} labels"))

        # Create Event Types
        for et_data in data['event_types']:
            EventType.objects.get_or_create(id=et_data['id'], defaults=et_data)
        self.stdout.write(self.style.SUCCESS(f"Created {len(data['event_types'])} event types"))

        # Create Bounding Box
        if data['bounding_box']:
            bb_data = data['bounding_box']
            # Ensure the related Algorithm exists
            Algorithm.objects.get_or_create(id=bb_data['algorithm_id'])
            BoundingBox.objects.get_or_create(id=bb_data['id'], defaults=bb_data)
            self.stdout.write(self.style.SUCCESS("Created 1 bounding box"))
        else:
            self.stdout.write(self.style.WARNING("No bounding box data found"))

        self.stdout.write(self.style.SUCCESS('Data loading completed successfully'))