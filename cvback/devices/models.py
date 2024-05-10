from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon
from django.core.validators import URLValidator
from encrypted_field import EncryptedField


class Area(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    name = models.CharField(max_length=255)
    area = Polygon()

    def __str__(self):
        return self.name


class Camera(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    primary_stream = EncryptedField(max_length=1024, validators=[URLValidator(schemes=['http', 'https', 'rtsp'])])
    location = models.PointField(default=Point(-70.60601882155144, -33.41260825941644, srid=4326))
    area = models.OneToOneField(Area, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class InferenceComputer(models.Model):
    added_date = models.DateTimeField("date created", auto_now_add=True)
    added_modified = models.DateTimeField("date modified", auto_now=True)
    enabled = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    location = models.PointField(default=Point(-70.69441297829056, -33.358564373936446, srid=4326))


    def __str__(self):
        return self.name
