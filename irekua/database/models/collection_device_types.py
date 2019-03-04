from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .schemas import Schema


class CollectionDeviceType(models.Model):
    collection = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection in which role applies'),
        blank=False,
        null=False)
    device_type = models.ForeignKey(
        'DeviceType',
        on_delete=models.PROTECT,
        db_column='device_type',
        verbose_name=_('device type'),
        help_text=_('Device to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for collection device metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.COLLECTION_DEVICE_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Device Type')
        verbose_name_plural = _('Collection Device Types')

    def __str__(self):
        msg = _('Device type {device} for collection {collection}').format(
            role=str(self.device_type),
            collection=str(self.collection))
        return msg

    def validate_metadata(self, metadata):
        try:
            self.metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for collection device. Error: {error}')
            msg = msg.format(error=str(error))
            raise ValidationError(msg)
