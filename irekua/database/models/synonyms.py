from django.contrib.postgres.fields import JSONField
from django.db import models


class Synonym(models.Model):
    source = models.ForeignKey(
        'Term',
        related_name='synonym_source',
        on_delete=models.CASCADE,
        blank=False)
    target = models.ForeignKey(
        'Term',
        related_name='synonym_target',
        on_delete=models.CASCADE,
        blank=False)
    metadata = JSONField(
        blank=True,
        null=True)
