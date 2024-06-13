from django.contrib.gis import admin
from .models import Area, Camera, InferenceComputer

# Register your models here.
admin.site.register(Area, admin.GISModelAdmin)
admin.site.register(Camera, admin.GISModelAdmin)
admin.site.register(InferenceComputer, admin.GISModelAdmin)
