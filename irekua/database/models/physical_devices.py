from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON
)


class PhysicalDevice(models.Model):
    serial_number = models.CharField(
        max_length=128,
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
        verbose_name=_('device'),
        help_text=_('Reference to type of device'),
        blank=False,
        null=False)
    owner = models.ForeignKey(
        'User',
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
        default=empty_JSON,
        null=True,
        blank=True)
    bundle = models.BooleanField(
        db_column='bundle',
        verbose_name=_('bundle'),
        help_text=_('Does this device possibly represents many physical devices?'),
        blank=False)

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
        verbose_name = _('Physical Device')
        verbose_name_plural = _('Physical Devices')

        ordering = ['device']

    def __str__(self):
        msg = _('Device %(id)s of type %(device)s')
        params = dict(
            id=self.id,
            device=str(self.device))
        return msg % params

    def clean(self):
        try:
            self.device.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(PhysicalDevice, self).clean()

    def validate_configuration(self, configuration):
        self.device.validate_configuration(configuration)
