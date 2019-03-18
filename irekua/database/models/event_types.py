from django.db import models
from django.core.exceptions import ValidationError
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
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Event type icon'),
        upload_to='images/event_types/',
        blank=True,
        null=True)

    label_term_types = models.ManyToManyField(
        'TermType',
        db_column='label_term_types',
        verbose_name=_('label term types'),
        help_text=_('Valid term types with which to label this type of events'),
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
        verbose_name = _('Event Type')
        verbose_name_plural = _('Event Types')

        ordering = ['name']

    def __str__(self):
        return self.name

    def validate_and_get_term_type(self, term_type):
        try:
            return self.label_term_types.get(name=term_type)
        except self.label_term_types.model.DoesNotExist:
            msg = _('Term type %(term_type)s is invalid for event type %(event_type)s')
            params = dict(term_type=str(term_type), event_type=str(self))
            raise ValidationError(msg, params=params)
