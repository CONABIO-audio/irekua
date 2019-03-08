from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_json,
    GENERIC_SAMPLING_EVENT,
)


class SamplingEvent(models.Model):
    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.PROTECT,
        db_column='sampling_event_type',
        verbose_name=_('sampling event type'),
        help_text=_('Type of sampling event'),
        blank=False,
        null=False,
        to_field='name',
        default=GENERIC_SAMPLING_EVENT)
    site = models.ForeignKey(
        'Site',
        db_column='site_id',
        verbose_name=_('site id'),
        help_text=_('Reference to site at which sampling took place'),
        on_delete=models.PROTECT,
        blank=True,
        null=True)
    device = models.ForeignKey(
        'PhysicalDevice',
        db_column='device_id',
        verbose_name=_('device id'),
        help_text=_('Reference to device used on sampling event'),
        on_delete=models.PROTECT,
        blank=False)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        default=empty_json,
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
        default=empty_json,
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

    class Meta:
        verbose_name = _('Sampling Event')
        verbose_name_plural = _('Sampling Events')

    def __str__(self):
        msg = _('Sampling event {id} on site {site}: {start} - {end}')
        msg = msg.format(
            id=self.id,
            site=str(self.site),
            start=self.started_on,
            end=self.ended_on)
        return msg

    def clean(self):
        try:
            self.sampling_event_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        try:
            self.sampling_event_type.validate_device_type(self.device.device.device_type)
        except ValidationError as error:
            raise ValidationError({'device': error})

        try:
            self.sampling_event_type.validate_site_type(self.site.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        try:
            self.device.validate_configuration(self.configuration)
        except ValidationError as error:
            raise ValidationError({'configuration': error})

        super(SamplingEvent, self).clean()
