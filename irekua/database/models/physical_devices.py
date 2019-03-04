from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    validate_json_instance,
    empty_json
)


class PhysicalDevice(models.Model):
    serial_number = models.CharField(
        max_length=100,
        db_column='serial_number',
        verbose_name=_('serial number'),
        help_text=_('Serial number of device'),
        blank=True,
        null=True,
        unique=True)
    device = models.ForeignKey(
        'Device',
        on_delete=models.PROTECT,
        db_column='device_id',
        verbose_name=_('device id'),
        help_text=_('Reference to type of device'),
        blank=False,
        null=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        db_column='owner_id',
        verbose_name=_('owner'),
        help_text=_('Owner of device'),
        null=True,
        blank=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to device'),
        default=empty_json,
        null=True,
        blank=True)
    bundle = models.BooleanField(
        db_column='bundle',
        verbose_name=_('bundle'),
        help_text=_('Does this device possibly represents many physical devices?'),
        blank=False)

    class Meta:
        verbose_name = _('Physical Device')
        verbose_name_plural = _('Physical Devices')

    def __str__(self):
        msg = _('Device {id} of type {device}').format(
            id=self.id,
            device=str(self.device))
        return msg

    def clean(self, *args, **kwargs):
        validate_json_instance(
            self.metadata,
            self.device.metadata_type.schema)
        super(PhysicalDevice, self).clean(*args, **kwargs)
