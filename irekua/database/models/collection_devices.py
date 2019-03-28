from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON,
)


class CollectionDevice(models.Model):
    device = models.ForeignKey(
        'PhysicalDevice',
        on_delete=models.PROTECT,
        db_column='device_id',
        verbose_name=_('device'),
        help_text=_('Reference to physical device'),
        blank=False,
        null=False)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which the device belongs'),
        blank=False,
        null=False)
    internal_id = models.CharField(
        max_length=64,
        db_column='internal_id',
        verbose_name=_('internal id'),
        help_text=_('ID of device within the collection'),
        blank=True)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_JSON,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated with device within collection'),
        null=True)

    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of creation of annotation'),
        editable=False,
        auto_now_add=True)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        editable=False,
        auto_now=True)

    class Meta:
        verbose_name = _('Collection Device')
        verbose_name_plural = _('Collection Devices')

    def __str__(self):
        msg = 'Device %(device_id)s from collection %(collection_id)s'
        params = dict(
            device_id=str(self.device),
            collection_id=str(self.collection))
        return msg % params

    def clean(self):
        try:
            device_type = self.collection.validate_and_get_device_type(
                self.device.device.device_type)
        except ValidationError as error:
            raise ValidationError({'device': str(error)})

        if device_type is not None:
            try:
                device_type.validate_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': str(error)})

        super(CollectionDevice, self).clean()
