from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema
from database.utils import (
    validate_json_instance,
    validate_is_of_collection,
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
    metadata_type = models.ForeignKey(
        'Schema',
        related_name='collection_device_metadata_type',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata_type'),
        help_text=_('JSON schema for metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.COLLECTION_DEVICE_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        blank=False,
        null=False,
        to_field='name',
        default=Schema.FREE_SCHEMA)
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

    def clean(self, *args, **kwargs):
        validate_is_of_collection(
            self.collection,
            self.metadata_type)
        validate_json_instance(
            self.metadata,
            self.metadata_type.schema)
        super(CollectionDevice, self).clean(*args, **kwargs)
