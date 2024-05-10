import os
from dotenv import load_dotenv
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

envs_path = os.path.join(os.path.dirname(__file__), '.envs/.local')

django_env_path = os.path.join(envs_path, '.django')
load_dotenv(django_env_path)

postgres_env_path = os.path.join(envs_path, '.postgres')
load_dotenv(postgres_env_path, override=True)

from cvback.devices.models import Area, Camera, InferenceComputer
from cvback.events.models import AreaOfInterest, BoundingBox, Inference, \
    InferenceDetectionClassification, InferenceClassification, Label, Event, Alert

fake = Faker()

def create_cameras(n):
    for _ in range(n):
        Camera.objects.create(
            name=fake.word(),
            enabled=fake.boolean(),
            primary_stream=fake.url(),
        )

def create_inference_computers(n):
    for _ in range(n):
        InferenceComputer.objects.create(
            name=fake.word(),
            enabled=fake.boolean(),
        )

def create_areas_of_interest(n):
    for _ in range(n):
        AreaOfInterest.objects.create(
            name=fake.word(),
            enabled=fake.boolean(),
            camera=Camera.objects.order_by('?').first(),  # Select random camera
            geometry=[[random.uniform(0, 1), random.uniform(0, 1)], [random.uniform(0, 1), random.uniform(0, 1)]],
            description=fake.text()
        )

def create_bounding_boxes(n):
    for _ in range(n):
        BoundingBox.objects.create(
            top_left=[random.uniform(0, 1), random.uniform(0, 1)],
            bottom_right=[random.uniform(0, 1), random.uniform(0, 1)],
            type=fake.word(),
            confidence=random.uniform(0, 1)
        )

def create_labels(n):
    for _ in range(n):
        Label.objects.create(
            model=fake.word(),
            label=fake.word()
        )

def create_inferences(n):
    for _ in range(n):
        label_instance = Label.objects.order_by('?').first()
        inference_computer_instance = InferenceComputer.objects.order_by('?').first()
        
        if inference_computer_instance and label_instance:
            if random.choice([True, False]):
                kind_value = 'dc'
                inference_instance = InferenceDetectionClassification(
                    inference_computer=inference_computer_instance,
                    kind=kind_value
                )
                # Save the instance to get an ID before adding many-to-many relationships
                inference_instance.save()

                bounding_box_instance = BoundingBox.objects.order_by('?').first()
                if bounding_box_instance:
                    inference_instance.bounding_boxes.add(bounding_box_instance)
                inference_instance.labels.add(label_instance)
            else:
                kind_value='cl'
                InferenceClassification.objects.create(
                    inference_computer=inference_computer_instance,
                    label=label_instance,
                    kind=kind_value
                )

def create_events(n):
    for _ in range(n):
        camera_instance = Camera.objects.order_by('?').first()

        # Randomly select between InferenceDetectionClassification and InferenceClassification
        if random.choice([True, False]):
            inference_instance = InferenceDetectionClassification.objects.order_by('?').first()
        else:
            inference_instance = InferenceClassification.objects.order_by('?').first()
        
        Event.objects.create(
            camera=camera_instance,
            inference_detection_classification=inference_instance if isinstance(inference_instance, InferenceDetectionClassification) else None,
            inference_classification=inference_instance if isinstance(inference_instance, InferenceClassification) else None,
            )

def create_alerts(n):
    for _ in range(n):
        Alert.objects.create(
            alert_type=random.choice(['telegram', 'sms']),
            recipient=fake.phone_number(),
            message=fake.text(),
            related_event=Event.objects.order_by('?').first()
        )

def data_exists():
    return Camera.objects.exists() or Event.objects.exists()


def main():
    if not data_exists():
        print("No data found, generating dummy data...")
        
        # Number of instances to create
        NUM_AREAS_OF_INTEREST = 20
        NUM_BOUNDING_BOXES = 20
        NUM_INFERENCES = 10
        NUM_EVENTS = 10
        NUM_LABELS = 10
        NUM_ALERTS = 10
        NUM_CAMERAS = 10
        NUM_INFERENCE_COMPUTER = 10

        create_cameras(NUM_CAMERAS)
        create_inference_computers(NUM_INFERENCE_COMPUTER)
        create_labels(NUM_LABELS)
        create_areas_of_interest(NUM_AREAS_OF_INTEREST)
        create_bounding_boxes(NUM_BOUNDING_BOXES)
        create_inferences(NUM_INFERENCES)
        create_events(NUM_EVENTS)
        create_alerts(NUM_ALERTS)

        print("Dummy data successfully created.")
    else:
        print("Dummy data already exists.")
