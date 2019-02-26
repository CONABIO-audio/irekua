from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class SamplingEvent(models.Model):
    device = models.ForeignKey(
        'PhysicalDevice',
        db_column='device_id',
        verbose_name=_('device id'),
        help_text=_('Reference to device used on sampling event'),
        on_delete=models.PROTECT,
        blank=False)
    configuration_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        related_name='sampling_event_configuration_type',
        db_column='configuration_type',
        verbose_name=_('configuration type'),
        help_text=_('Schema for sampling event configuration'),
        limit_choices_to=(
            models.Q(field__exact='sampling_configuration_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    configuration = JSONField(
        db_column='configuration',
        verbose_name=_('configuration'),
        help_text=_('Configuration on device through the sampling event'),
        blank=True,
        null=True)
    commentaries = models.TextField(
        db_column='commentaries',
        verbose_name=_('commentaries'),
        help_text=_('Sampling event commentaries'),
        blank=True)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        related_name='sampling_event_metadata_type',
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for sampling event metadata'),
        limit_choices_to=(
            models.Q(field__exact='sampling_event_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to sampling event'),
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
    site = models.ForeignKey(
        'Site',
        db_column='site_id',
        verbose_name=_('site id'),
        help_text=_('Reference to site at which sampling took place'),
        on_delete=models.PROTECT,
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
