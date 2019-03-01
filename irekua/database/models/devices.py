from django.db import models
from django.utils.translation import gettext_lazy as _


class Device(models.Model):
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        related_name='device_type',
        db_column='device_type',
        verbose_name=_('device type'),
        help_text=_('Type of device'),
        limit_choices_to={'term_type': 'device_type'},
        blank=False)
    brand = models.ForeignKey(
        'DeviceBrand',
        on_delete=models.PROTECT,
        related_name='device_brand',
        db_column='brand',
        verbose_name=_('brand'),
        help_text=_('Brand of device'),
        limit_choices_to={'term_type': 'brand'},
        blank=False)
    model = models.CharField(
        max_length=64,
        db_column='model',
        verbose_name=_('model'),
        help_text=_('Model of device'),
        blank=False)

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        unique_together = (('brand', 'model'))

    def __str__(self):
        msg = '{device_type}: {brand} - {model}'.format(
            device_type=self.device_type,
            brand=self.brand,
            model=self.model)
        return msg
