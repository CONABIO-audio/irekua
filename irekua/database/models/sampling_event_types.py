from django.db import models
from django.utils.translation import gettext_lazy as _

from .schemas import Schema


class SamplingEventType(models.Model):
    name = models.CharField(
        max_length=128,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name fo sampling event type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of sampling event type'),
        blank=True)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for sampling event type'),
        upload_to='images/sampling_event_types/',
        blank=True,
        null=True)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('Schema for metadata for sampling event of this type'),
        limit_choices_to=(
            models.Q(field__exact=Schema.SAMPLING_EVENT_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    restrict_device_types = models.BooleanField(
        db_column='restrict_device_types',
        verbose_name=_('restrict device types'),
        help_text=_('Flag indicating whether to restrict device types associated with this sampling event type'),
        default=False,
        blank=False,
        null=False)
    restrict_site_types = models.BooleanField(
        db_column='restrict_site_types',
        verbose_name=_('restrict site types'),
        help_text=_('Flag indicating whether to restrict site types associated with this sampling event type'),
        default=False,
        blank=False,
        null=False)

    device_types = models.ManyToManyField(
        'DeviceType',
        db_column='device_types',
        verbose_name=_('device types'),
        help_text=_('Valid device types for this sampling event type'))
    site_types = models.ManyToManyField(
        'SiteType',
        db_column='site_types',
        verbose_name=_('site types'),
        help_text=_('Valid site types for this sampling event type'))

    class Meta:
        verbose_name = _('Sampling Event Type')
        verbose_name_plural = _('Sampling Event Types')

    def __str__(self):
        return self.name
