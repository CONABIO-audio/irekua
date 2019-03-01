from django.db import models
from django.utils.translation import gettext_lazy as _


class CollectionSchema(models.Model):
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection id'),
        help_text=_('Collection in which schema applies'),
        blank=False,
        null=False)
    schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='schema_id',
        verbose_name=_('schema id'),
        help_text=_('Schema to be part of collection'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Schema')
        verbose_name_plural = _('Collection Schemas')

    def __str__(self):
        msg = _('Schema {schema} for collection {collection}').format(
                schema=str(self.schema),
                collection=str(self.collection))
        return msg
