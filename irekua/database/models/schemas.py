from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Schema(models.Model):
    JSON_FIELDS = [
        ('annotation_label', _('annotation label')),
        ('annotation_annotation', _('annotation annotation')),
        ('annotation_metadata', _('annotation metadata')),
        ('collection_metadata', _('collection metadata')),
        ('collection_device_metadata', _('collection device metadata')),
        ('collection_site_metadata', _('collection site metadata')),
        ('collection_user_metadata', _('collection user metadata')),
        ('device_metadata', _('device metadata')),
        ('entailment_metadata', _('entailment metadata')),
        ('item_media_info', _('item media info')),
        ('item_metadata', _('item metadata')),
        ('licence_metadata', _('licence metadata')),
        ('model_metadata', _('model metadata')),
        ('sampling_event_configuration', _('sampling event configuration')),
        ('sampling_event_metadata', _('sampling event metadata')),
        ('secondary_item_media_info', _('secondary item media info')),
        ('site_metadata', _('site metadata')),
        ('synonym_metadata', _('synonym metadata')),
        ('term_metadata', _('term metadata')),
        ('user_metadata', _('user metadata')),
        ('global', _('global')),
    ]

    field = models.CharField(
        max_length=64,
        blank=False,
        db_column='field',
        verbose_name=_('field'),
        help_text=_('Field to which JSON schema applies'),
        null=False,
        choices=JSON_FIELDS)
    name = models.CharField(
        max_length=30,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of JSON schema'),
        unique=True,
        blank=False,
        null=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of schema'),
        blank=True)
    schema = JSONField(
        blank=False,
        db_column='schema',
        verbose_name=_('schema'),
        help_text=_('JSON object with schema'),
        null=False)

    class Meta:
        verbose_name = _('Schema')
        verbose_name_plural = _('Schemas')

    def __str__(self):
        return self.name
