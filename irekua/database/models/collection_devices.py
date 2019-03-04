from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_json,
)


class CollectionDevice(models.Model):
    device = models.ForeignKey(
        'PhysicalDevice',
        on_delete=models.PROTECT,
        db_column='device_id',
        verbose_name=_('device id'),
        help_text=_('Reference to physical device'),
        blank=False,
        null=False)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection id'),
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
        default=empty_json,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated with device within collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection Device')
        verbose_name_plural = _('Collection Devices')

    def __str__(self):
        msg = 'Device {device_id} from collection {collection_id}'.format(
            device_id=str(self.device),
            collection_id=str(self.collection))
        return msg

    def clean(self):
        try:
            self.collection.validate_device_type(self.device.device_type)
        except ValidationError as error:
            raise ValidationError({'device': str(error)})

        try:
            self.collection.validate_device_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': str(error)})

        super(CollectionDevice, self).clean()
