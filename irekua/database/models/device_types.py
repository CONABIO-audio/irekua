from django.db import models
from django.utils.translation import gettext_lazy as _


class DeviceType(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name for device type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of device type'),
        blank=False)
    icon = models.ImageField(
        db_column='icon',
        verbose_name=_('icon'),
        help_text=_('Icon for device type'),
        upload_to='images/device_types/',
        blank=True,
        null=True)

    class Meta:
        verbose_name = _('Device Type')
        verbose_name_plural = _('Device Types')

    def __str__(self):
        return self.name
