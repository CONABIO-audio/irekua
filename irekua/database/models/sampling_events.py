from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON,
)


class SamplingEvent(models.Model):
    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.PROTECT,
        db_column='sampling_event_type',
        verbose_name=_('sampling event type'),
        help_text=_('Type of sampling event'),
        blank=False,
        null=False)
    site = models.ForeignKey(
        'Site',
        db_column='site_id',
        verbose_name=_('site'),
        help_text=_('Reference to site at which sampling took place'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    physical_device = models.ForeignKey(
        'PhysicalDevice',
        db_column='physical_device_id',
        verbose_name=_('physical device'),
        help_text=_('Reference to physical device used on sampling event'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        default=empty_JSON,
        help_text=_('Configuration on device through the sampling event'),
        blank=True,
        null=True)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event'),
        default=empty_JSON,
        blank=True,
        null=True)
    started_on = models.DateTimeField(
        db_column='started_on',
        verbose_name=_('started on'),
        help_text=_('Date at which sampling begun'),
        blank=True,
        null=True)
    ended_on = models.DateTimeField(
        db_column='ended_on',
        verbose_name=_('ended on'),
        help_text=_('Date at which sampling stoped'),
        blank=True,
        null=True)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.PROTECT,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which sampling event belongs'),
        blank=False,
        null=False)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence for all items in sampling event'),
        blank=True,
        null=True)

    created_by = models.ForeignKey(
        'User',
        related_name='sampling_event_created_by',
        on_delete=models.PROTECT,
        db_column='created_by',
        verbose_name=_('create by'),
        help_text=_('Creator of sampling event'),
        blank=False,
        null=False)
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
    modified_by = models.ForeignKey(
        'User',
        related_name='sampling_event_modified_by',
        on_delete=models.PROTECT,
        db_column='modified_by',
        verbose_name=_('modified by'),
        help_text=_('Last modifier'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Sampling Event')
        verbose_name_plural = _('Sampling Events')

        ordering = ['-started_on']

    def __str__(self):
        msg = _('Sampling event {id} on site {site}: {start} - {end}')
        msg = msg.format(
            id=str(self.id),
            site=str(self.site),
            start=str(self.started_on),
            end=str(self.ended_on))
        return msg

    def clean(self):
        try:
            self.sampling_event_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        try:
            self.sampling_event_type.validate_device_type(
                self.device.device.device_type)
        except ValidationError as error:
            raise ValidationError({'device': error})

        try:
            self.sampling_event_type.validate_site_type(self.site.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        try:
            self.physical_device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error})

        super(SamplingEvent, self).clean()
