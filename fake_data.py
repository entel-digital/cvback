import os
from dotenv import load_dotenv
import django
import random
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

# Ruta al directorio de archivos .envs
envs_path = os.path.join(os.path.dirname(__file__), '.envs/.local')

# Variable de entorno del archivo .django
django_env_path = os.path.join(envs_path, '.django')
load_dotenv(django_env_path)

# Variable de entorno del archivo .postgres
postgres_env_path = os.path.join(envs_path, '.postgres')
load_dotenv(postgres_env_path, override=True)

from cvback.devices.models import Camera, InferenceComputer
from cvback.events.models import AreaOfInterest, BoundingBox, Inference, Event, Alert

# Instancia de Faker
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
            camera=Camera.objects.order_by('?').first(),  # Selecciona una cámara aleatoria
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

def create_inferences(n):
    for _ in range(n):
        Inference.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            bounding_boxes=BoundingBox.objects.order_by('?').first()
        )

def create_events(n):
    for _ in range(n):
        Event.objects.create(
            camera=Camera.objects.order_by('?').first(),
            inference=Inference.objects.order_by('?').first()
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

if not data_exists():
    print("No se encontraron datos, generando datos ficticios...")
    
    # Número de instancias a crear
    NUM_AREAS_OF_INTEREST = 20
    NUM_BOUNDING_BOXES = 20
    NUM_INFERENCES = 10
    NUM_EVENTS = 10
    NUM_ALERTS = 10
    NUM_CAMERAS = 10
    NUM_INFERENCE_COMPUTER = 10

    create_cameras(NUM_CAMERAS)
    create_inference_computers(NUM_INFERENCE_COMPUTER)
    create_areas_of_interest(NUM_AREAS_OF_INTEREST)
    create_bounding_boxes(NUM_BOUNDING_BOXES)
    create_inferences(NUM_INFERENCES)
    create_events(NUM_EVENTS)
    create_alerts(NUM_ALERTS)

    print("Datos ficticios creados exitosamente.")
else:
    print("Ya existen datos ficticios.")
