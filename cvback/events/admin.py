from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AreaOfInterest)
admin.site.register(BoundingBox)
admin.site.register(Event)
admin.site.register(Algorithm)
admin.site.register(Label)
admin.site.register(InferenceDetectionClassification)
admin.site.register(InferenceClassification)