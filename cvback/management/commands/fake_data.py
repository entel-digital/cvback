import os
from dotenv import load_dotenv
import django
import random
from faker import Faker
from django.contrib.gis.geos import Polygon

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

envs_path = os.path.join(os.path.dirname(__file__), '.envs/.local')

django_env_path = os.path.join(envs_path, '.django')
load_dotenv(django_env_path)

postgres_env_path = os.path.join(envs_path, '.postgres')
load_dotenv(postgres_env_path, override=True)

from cvback.devices.models import Area, Camera, InferenceComputer
from cvback.events.models import (
    AreaOfInterest, LineOfInterest, Algorithm, Label, Frame, KeyFrames, Video, KeyVideos,
    BoundingBox, InferenceOCR, KeyInferenceOCR, InferenceDetectionClassification,
    KeyInferenceDetectionClassification, InferenceDetectionClassificationTracker,
    KeyInferenceDetectionClassificationTracker, InferenceClassification,
    KeyInferenceClassification, EventType, Event)

fake = Faker()

def generate_random_polygon():
    coordinates = [(fake.longitude(), fake.latitude()) for _ in range(4)]
    coordinates.append(coordinates[0])
    return Polygon(coordinates)

def create_areas(n):
    for _ in range(n):
        area_polygon = generate_random_polygon()
        Area.objects.create(
            name=fake.word(),
            area=area_polygon
        )

def create_cameras(n):
    for _ in range(n):
        Camera.objects.create(
            name=fake.word(),
            enabled=fake.boolean(),
            primary_stream=fake.url(),
            #area=area_polygon
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

def create_lines_of_interest(n):
    for _ in range(n):
        LineOfInterest.objects.create(
            name=fake.word(),
            enabled=fake.boolean(),
            camera=Camera.objects.order_by('?').first(),
            geometry=[random.uniform(0, 1), random.uniform(0, 1)],
            description=fake.text()
        )

def create_algorithms(n):
    for _ in range(n):
        Algorithm.objects.create(
            kind=random.choice(Algorithm.ALGORITHM_CHOICES)[0],
            name=fake.word(),
            version=f"{random.randint(0,99)}.{random.randint(0,99)}.{random.randint(0,999)}",
            repository=fake.url()
        )

from django.db import IntegrityError

def create_labels(n):
    created_labels = 0
    attempts = 0
    max_attempts = n * 3 
    while created_labels < n and attempts < max_attempts:
        try:
            name = fake.unique.word()
            Label.objects.create(
                name=name,
                color_group=random.choice(Label.COLOR_GROUP_CHOICES)[0]
            )
            created_labels += 1
        except IntegrityError:
            pass
        attempts += 1

    if created_labels < n:
        print(f"Warning: Only created {created_labels} labels out of {n} requested due to uniqueness constraints.")

def create_frames(n):
    for _ in range(n):
        frame = Frame.objects.create(
            image=fake.file_path(extension='jpg')
        )
        frame.cameras.set(Camera.objects.order_by('?')[:random.randint(1, 3)])

def create_key_frames(n):
    for _ in range(n):
        key_frame = KeyFrames.objects.create(
            name=fake.word()
        )
        key_frame.frames.set(Frame.objects.order_by('?')[:random.randint(1, 5)])

def create_videos(n):
    for _ in range(n):
        video = Video.objects.create(
            video=fake.file_path(extension='mp4')
        )
        video.cameras.set(Camera.objects.order_by('?')[:random.randint(1, 3)])

def create_key_videos(n):
    for _ in range(n):
        key_video = KeyVideos.objects.create(
            name=fake.word()
        )
        key_video.frames.set(Video.objects.order_by('?')[:random.randint(1, 5)])

def create_bounding_boxes(n):
    for _ in range(n):
        BoundingBox.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            algorithm=Algorithm.objects.order_by('?').first(),
            confidence=random.uniform(0, 1),
            top_left=[random.uniform(0, 1), random.uniform(0, 1)],
            bottom_right=[random.uniform(0, 1), random.uniform(0, 1)]
        )

def create_inference_ocr(n):
    for _ in range(n):
        InferenceOCR.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            algorithm=Algorithm.objects.order_by('?').first(),
            confidence=random.uniform(0, 1),
            name=fake.word(),
            value=fake.text()
        )

def create_key_inference_ocr(n):
    for _ in range(n):
        KeyInferenceOCR.objects.create(
            name=fake.word(),
            inferences=InferenceOCR.objects.order_by('?').first()
        )

def create_inference_detection_classification(n):
    for _ in range(n):
        inference = InferenceDetectionClassification.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            algorithm=Algorithm.objects.order_by('?').first(),
            confidence=random.uniform(0, 1)
        )
        inference.bounding_boxes.set(BoundingBox.objects.order_by('?')[:random.randint(1, 5)])
        inference.labels.set(Label.objects.order_by('?')[:random.randint(1, 5)])

def create_key_inference_detection_classification(n):
    for _ in range(n):
        KeyInferenceDetectionClassification.objects.create(
            name=fake.word(),
            inferences=InferenceDetectionClassification.objects.order_by('?').first()
        )

def create_inference_detection_classification_tracker(n):
    for _ in range(n):
        inference = InferenceDetectionClassificationTracker.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            algorithm=Algorithm.objects.order_by('?').first(),
            confidence=random.uniform(0, 1),
            tracking_ids=[random.randint(1, 1000) for _ in range(random.randint(1, 5))]
        )
        inference.bounding_boxes.set(BoundingBox.objects.order_by('?')[:random.randint(1, 5)])
        inference.labels.set(Label.objects.order_by('?')[:random.randint(1, 5)])

def create_key_inference_detection_classification_tracker(n):
    for _ in range(n):
        KeyInferenceDetectionClassificationTracker.objects.create(
            name=fake.word(),
            inferences=InferenceDetectionClassificationTracker.objects.order_by('?').first()
        )

def create_inference_classification(n):
    for _ in range(n):
        InferenceClassification.objects.create(
            inference_computer=InferenceComputer.objects.order_by('?').first(),
            algorithm=Algorithm.objects.order_by('?').first(),
            confidence=random.uniform(0, 1),
            label=Label.objects.order_by('?').first()
        )

def create_key_inference_classification(n):
    for _ in range(n):
        KeyInferenceClassification.objects.create(
            name=fake.word(),
            inferences=InferenceClassification.objects.order_by('?').first()
        )

def create_event_types(n):
    for _ in range(n):
        EventType.objects.create(
            name=fake.word(),
            version=f"{random.randint(0,99)}.{random.randint(0,99)}.{random.randint(0,999)}",
            documentation=fake.file_path(extension='pdf')
        )

def create_events(n):
    for _ in range(n):
        event = Event.objects.create(
            event_type=EventType.objects.order_by('?').first(),
            confidence=random.uniform(0, 1)
        )
        event.cameras.set(Camera.objects.order_by('?')[:random.randint(1, 3)])
        event.frames.set(Frame.objects.order_by('?')[:random.randint(1, 5)])
        event.key_frames.set(KeyFrames.objects.order_by('?')[:random.randint(1, 3)])
        event.videos.set(Video.objects.order_by('?')[:random.randint(1, 3)])
        event.key_videos.set(KeyVideos.objects.order_by('?')[:random.randint(1, 3)])
        event.labels_detected.set(Label.objects.order_by('?')[:random.randint(1, 5)])
        event.labels_missing.set(Label.objects.order_by('?')[:random.randint(1, 5)])
        event.inference_classification.set(InferenceClassification.objects.order_by('?')[:random.randint(1, 3)])
        event.inference_detection_classification = InferenceDetectionClassification.objects.order_by('?').first()
        event.inference_detection_classification_tracker.set(InferenceDetectionClassificationTracker.objects.order_by('?')[:random.randint(1, 3)])
        event.inference_ocr.set(InferenceOCR.objects.order_by('?')[:random.randint(1, 3)])
        event.key_inference_classification.set(KeyInferenceClassification.objects.order_by('?')[:random.randint(1, 3)])
        event.key_inference_detection_classification.set(KeyInferenceDetectionClassification.objects.order_by('?')[:random.randint(1, 3)])
        event.key_inference_detection_classification_tracker.set(KeyInferenceDetectionClassificationTracker.objects.order_by('?')[:random.randint(1, 3)])
        event.key_inference_ocr.set(KeyInferenceOCR.objects.order_by('?')[:random.randint(1, 3)])

def data_exists():
    return Camera.objects.exists() or Event.objects.exists()


def main():
    if not data_exists():
        print("No data found, generating dummy data...")
        
        NUM_AREAS = 10
        NUM_CAMERAS = 10
        NUM_INFERENCE_COMPUTERS = 10
        NUM_AREAS_OF_INTEREST = 10
        NUM_LINES_OF_INTEREST = 10
        NUM_ALGORITHMS = 10
        NUM_LABELS = 10
        NUM_FRAMES = 10
        NUM_KEY_FRAMES = 10
        NUM_VIDEOS = 10
        NUM_KEY_VIDEOS = 10
        NUM_BOUNDING_BOXES = 10
        NUM_INFERENCE_OCR = 10
        NUM_KEY_INFERENCE_OCR = 10
        NUM_INFERENCE_DETECTION_CLASSIFICATION = 10
        NUM_KEY_INFERENCE_DETECTION_CLASSIFICATION = 10
        NUM_INFERENCE_DETECTION_CLASSIFICATION_TRACKER = 10
        NUM_KEY_INFERENCE_DETECTION_CLASSIFICATION_TRACKER = 10
        NUM_INFERENCE_CLASSIFICATION = 10
        NUM_KEY_INFERENCE_CLASSIFICATION = 10
        NUM_EVENT_TYPES = 10
        NUM_EVENTS = 10

        #create_areas(NUM_AREAS)
        create_cameras(NUM_CAMERAS)
        create_inference_computers(NUM_INFERENCE_COMPUTERS)
        create_areas_of_interest(NUM_AREAS_OF_INTEREST)
        create_lines_of_interest(NUM_LINES_OF_INTEREST)
        create_algorithms(NUM_ALGORITHMS)
        create_labels(NUM_LABELS)
        create_frames(NUM_FRAMES)
        create_key_frames(NUM_KEY_FRAMES)
        create_videos(NUM_VIDEOS)
        create_key_videos(NUM_KEY_VIDEOS)
        create_bounding_boxes(NUM_BOUNDING_BOXES)
        create_inference_ocr(NUM_INFERENCE_OCR)
        create_key_inference_ocr(NUM_KEY_INFERENCE_OCR)
        create_inference_detection_classification(NUM_INFERENCE_DETECTION_CLASSIFICATION)
        create_key_inference_detection_classification(NUM_KEY_INFERENCE_DETECTION_CLASSIFICATION)
        create_inference_detection_classification_tracker(NUM_INFERENCE_DETECTION_CLASSIFICATION_TRACKER)
        create_key_inference_detection_classification_tracker(NUM_KEY_INFERENCE_DETECTION_CLASSIFICATION_TRACKER)
        create_inference_classification(NUM_INFERENCE_CLASSIFICATION)
        create_key_inference_classification(NUM_KEY_INFERENCE_CLASSIFICATION)
        create_event_types(NUM_EVENT_TYPES)
        create_events(NUM_EVENTS)

        print("Dummy data successfully created.")
    else:
        print("Dummy data already exists.")

if __name__ == "__main__":
    main()