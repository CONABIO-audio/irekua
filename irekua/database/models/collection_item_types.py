from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .schemas import Schema


class CollectionItemType(models.Model):
    collection_type = models.ForeignKey(
        'CollectionType',
        on_delete=models.CASCADE,
        db_column='collection_type_id',
        verbose_name=_('collection type'),
        help_text=_('Collection type in which role applies'),
        blank=False,
        null=False)
    item_type = models.ForeignKey(
        'ItemType',
        on_delete=models.PROTECT,
        db_column='item_type_id',
        verbose_name=_('item type'),
        help_text=_('Item to be part of collection'),
        blank=False,
        null=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('JSON schema for collection item metadata'),
        limit_choices_to=(
            models.Q(field__exact=Schema.ITEM_METADATA) |
            models.Q(field__exact=Schema.GLOBAL)),
        to_field='name',
        default=Schema.FREE_SCHEMA,
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Item Type')
        verbose_name_plural = _('Collection Item Types')

    def __str__(self):
        msg = _('Item type %(item)s for collection %(collection)s')
        params = dict(role=str(self.item_type), collection=str(self.collection_type))
        return msg % params

    def validate_metadata(self, metadata):
        try:
            self.metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid metadata for item type %(type)s in collection %(collection). Error: %(error)')
            params = dict(
                type=str(self.item_type),
                collection_type=str(self.collection_type),
                error=str(error))
            raise ValidationError(msg, params=params)
