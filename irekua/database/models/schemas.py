from django.contrib.postgres.fields import JSONField
from django.db import models


class Schema(models.Model):
    JSON_FIELDS = [
        ('annotation_label', 'annotation_label'),
        ('annotation_annotation', 'annotation_annotation'),
        ('annotation_metadata', 'annotation_metadata'),
        ('collection_metadata', 'collection_metadata'),
        ('device_metadata', 'device_metadata'),
        ('entailment_metadata', 'entailment_metadata'),
        ('item_media_info', 'item_media_info'),
        ('item_metadata', 'item_metadata'),
        ('licence_metadata', 'licence_metadata'),
        ('model_metadata', 'model_metadata'),
        ('sampling_event_configuration', 'sampling_event_configuration'),
        ('sampling_event_metadata', 'sampling_event_metadata'),
        ('secondary_item_media_info', 'secondary_item_media_info'),
        ('site_metadata', 'site_metadata'),
        ('synonym_metadata', 'synonym_metadata'),
        ('term_metadata', 'term_metadata'),
        ('user_metadata', 'user_metadata'),
    ]

    field = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        choices=JSON_FIELDS)
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False)
    description = models.TextField(
        blank=True)
    schema = JSONField(
        blank=False,
        null=False)
