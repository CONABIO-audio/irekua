from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class DeviceTerm(models.Model):
    DEVICE_FIELDS = [
        ('device_type', _('device type')),
        ('brand', _('brand')),
    ]

    term_type = models.CharField(
        max_length=16,
        choices=DEVICE_FIELDS,
        db_column='term_type',
        verbose_name=_('term type'),
        help_text=_('Type of term'),
        blank=False)
    value = models.CharField(
        max_length=128,
        db_column='value',
        verbose_name=_('value'),
        help_text=_('Admissible value for type of term'))
    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_column='added_by',
        verbose_name=_('added by'),
        help_text=_('User that uploaded this term'),
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Device Term')
        verbose_name_plural = _('Device Terms')
        unique_together = (('term_type', 'value'))

    def __str__(self):
        msg = '{term_type}: {value}'.format(
            term_type=self.term_type,
            value=self.value)
        return msg
