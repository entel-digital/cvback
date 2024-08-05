from django.contrib import admin
from .models import (AreaOfInterest, LineOfInterest, BoundingBox, Event, Algorithm, Label, Frame,
                     Video, KeyFrame, KeyVideo, EventType, InferenceClassification, InferenceDetectionClassification,
                     InferenceDetectionClassificationTracker, InferenceOCR)

# Register your models here.
admin.site.register(AreaOfInterest)
admin.site.register(LineOfInterest)
admin.site.register(BoundingBox)
admin.site.register(Event)
admin.site.register(Algorithm)
admin.site.register(Label)
admin.site.register(Frame)
admin.site.register(Video)
admin.site.register(KeyFrame)
admin.site.register(KeyVideo)
admin.site.register(EventType)
# admin.site.register()
# admin.site.register()
# admin.site.register()

admin.site.register(InferenceDetectionClassification)
admin.site.register(InferenceClassification)
admin.site.register(InferenceDetectionClassificationTracker)
admin.site.register(InferenceOCR)
