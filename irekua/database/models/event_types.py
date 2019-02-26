from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(models.Model):
    name = models.CharField(
        max_length=64,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of event type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of event type'),
        blank=False)

    class Meta:
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')

    def __str__(self):
        return self.name
