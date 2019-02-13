from django.contrib.postgres.fields import JSONField
from django.db import models


class SamplingEvent(models.Model):
    device = models.ForeignKey(
        'Device',
        on_delete=models.PROTECT,
        blank=False)
    configuration = JSONField(
        blank=False)
    commentaries = models.TextField(
        blank=True)
    metadata = JSONField(
        blank=True,
        null=True)
    started_on = models.DateTimeField(
        blank=True,
        null=True)
    ended_on = models.DateTimeField(
        blank=True,
        null=True)
    site = models.ForeignKey(
        'Site',
        on_delete=models.PROTECT,
        blank=True,
        null=True)
