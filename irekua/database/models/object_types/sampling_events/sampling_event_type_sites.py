from django.db import models
from django.utils.translation import gettext_lazy as _


class SamplingEventTypeSiteType(models.Model):
    sampling_event_type = models.ForeignKey(
        'SamplingEventType',
        on_delete=models.CASCADE,
        db_column='sampling_event_type_id',
        verbose_name=_('sampling event type'),
        help_text=_(
            'Sampling event type in which this site '
            'type can be used'),
        null=False,
        blank=False)
    site_type = models.ForeignKey(
        'SiteType',
        on_delete=models.PROTECT,
        db_column='site_type_id',
        verbose_name=_('site type'),
        help_text=_(
            'Type of site that can be used in sampling '
            'event of the given type'),
        null=False,
        blank=False)

    class Meta:
        verbose_name = _('Sampling Event Type Site Type')
        verbose_name_plural = _('Sampling Event Type Site Types')

        ordering = ['sampling_event_type']
        unique_together = (
            ('sampling_event_type', 'site_type'),
        )
