from django.contrib.postgres.fields import JSONField
from django.db import models


class Term(models.Model):
    type = models.CharField(
        max_length=50,
        blank=False)
    value = models.CharField(
        max_length=50,
        blank=False)
    description = models.TextField(
        blank=True)
    metadata = JSONField(
        blank=True,
        null=True)
