from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


class Device(models.Model):
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        related_name='device_type',
        db_column='device_type',
        verbose_name=_('device type'),
        help_text=_('Type of device'),
        blank=False)
    brand = models.ForeignKey(
        'DeviceBrand',
        on_delete=models.PROTECT,
        related_name='device_brand',
        db_column='brand',
        verbose_name=_('brand'),
        help_text=_('Brand of device'),
        blank=False)
    model = models.CharField(
        max_length=64,
        db_column='model',
        verbose_name=_('model'),
        help_text=_('Model of device'),
        blank=False)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        related_name='device_metadata_type',
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for device metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.DEVICE_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)
    configuration_type = models.ForeignKey(
        'Schema',
        related_name='device_configuration_type',
        on_delete=models.PROTECT,
        db_column='configuration_type',
        verbose_name=_('configuration type'),
        help_text=_('JSON schema for device configuration'),
        limit_choices_to=(
            models.Q(field__exact=Schema.DEVICE_CONFIGURATION) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

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
