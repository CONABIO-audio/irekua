from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import JSONField

from database.utils import (
    validate_JSON_schema,
    validate_JSON_instance,
    simple_JSON_schema,
)


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
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata schema'),
        help_text=_('JSON Schema for metadata of sampling event info'),
        blank=True,
        null=False,
        default=simple_JSON_schema,
        validators=[validate_JSON_schema])

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
        help_text=_('Valid device types for this sampling event type'),
        blank=True)
    site_types = models.ManyToManyField(
        'SiteType',
        db_column='site_types',
        verbose_name=_('site types'),
        help_text=_('Valid site types for this sampling event type'),
        blank=True)

    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of entry creation'),
        auto_now_add=True,
        editable=False)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        auto_now=True,
        editable=False)

    class Meta:
        verbose_name = _('Sampling Event Type')
        verbose_name_plural = _('Sampling Event Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_metadata(self, metadata):
        try:
            validate_JSON_instance(
                schema=self.metadata_schema,
                instance=metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for sampling event of type %(type)s. Error: %(error)')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)

    def validate_device_type(self, device_type):
        if not self.restrict_device_types:
            return

        try:
            self.device_types.get(name=device_type.name)
        except self.device_types.model.DoesNotExist:
            msg = _('Device type %(device_type) is not valid for sampling event of type %(type)s')
            params = dict(device_type=str(device_type), type=str(self))
            raise ValidationError(msg, params=params)

    def validate_site_type(self, site_type):
        if not self.restrict_site_types:
            return

        try:
            self.site_types.get(name=site_type.name)
        except self.site_types.model.DoesNotExist:
            msg = _('Site type %(site_type) is not valid for sampling event of type %(type)s')
            params = dict(site_type=str(site_type), type=str(self))
            raise ValidationError(msg, params=params)
