from django.contrib.postgres.fields import JSONField
from django.db import models


class Licence(models.Model):
    name = models.CharField(
        max_length=70,
        blank=False)
    description = models.TextField(
        blank=False)
    document = models.CharField(
        max_length=70,
        blank=True)
    public = models.BooleanField(
        blank=False,
        null=False)
    created_on = models.DateTimeField(
        blank=False)
    valid_until = models.DateTimeField(
        blank=True,
        null=True)
    metadata = JSONField(
        blank=True,
        null=True)
