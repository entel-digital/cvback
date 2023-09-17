from django.contrib.gis import admin
from .models import Camera, InferenceComputer

# Register your models here.
admin.site.register(Camera, admin.GISModelAdmin)
admin.site.register(InferenceComputer, admin.GISModelAdmin)
