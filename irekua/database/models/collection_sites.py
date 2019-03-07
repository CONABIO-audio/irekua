from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_json,
)


class CollectionSite(models.Model):
    site = models.ForeignKey(
        'Site',
        on_delete=models.PROTECT,
        db_column='site_id',
        verbose_name=_('site'),
        help_text=_('Reference to Site'),
        blank=False,
        null=False)
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection to which the site belongs'),
        blank=False,
        null=False)
    internal_id = models.CharField(
        max_length=64,
        db_column='internal_id',
        verbose_name=_('internal id'),
        help_text=_('ID of site within the collection'),
        blank=True)
    metadata = JSONField(
        blank=True,
        db_column='metadata',
        default=empty_json,
        verbose_name=_('metadata'),
        help_text=_('Metadata associated with site within collection'),
        null=True)

    class Meta:
        verbose_name = _('Collection Site')
        verbose_name_plural = _('Collection Sites')
        unique_together = (('collection', 'internal_id'))

    def __str__(self):
        msg = _('Site %(site)s of collection %(collection)')
        params = dict(
            site=str(self.site),
            collection=str(self.collection))
        return msg % params

    def clean(self):
        try:
            site_type = self.collection.validate_and_get_site_type(self.site.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        if site_type is not None:
            try:
                self.collection.validate_site_metadata(self.metadata)
            except ValidationError as error:
                raise ValidationError({'metadata': error})
        super(CollectionSite, self).clean()
