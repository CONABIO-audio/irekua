from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db.models import PointField
from django.db import models


class Site(models.Model):
    name = models.CharField(
        max_length=70,
        blank=True)
    geo_ref = PointField(
        blank=False,
        spatial_index=True)
    latitude = models.FloatField(
        blank=False)
    longitude = models.FloatField(
        blank=False)
    altitude = models.FloatField(
        blank=True,
        null=True)
    metadata = JSONField(
        blank=True,
        null=True)
