from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON

from database.models.base import IrekuaModelBaseUser


class CollectionSite(IrekuaModelBaseUser):
    site_type = models.ForeignKey(
        'SiteType',
        on_delete=models.PROTECT,
        db_column='site_type',
        verbose_name=_('site type'),
        help_text=_('Type of site'),
        blank=False,
        null=False)
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
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to site in collection'),
        default=empty_JSON,
        blank=True,
        null=True)
    internal_id = models.CharField(
        max_length=64,
        db_column='internal_id',
        verbose_name=_('internal id'),
        help_text=_('ID of site within the collection'),
        blank=True)

    class Meta:
        verbose_name = _('Collection Site')
        verbose_name_plural = _('Collection Sites')

        unique_together = (
            ('collection', 'site'),
            ('collection', 'internal_id'),
        )

    def __str__(self):
        msg = _('Site %(site)s of collection %(collection)s')
        params = dict(
            site=str(self.site),
            collection=str(self.collection))
        return msg % params

    def clean(self):
        try:
            self.collection.validate_and_get_site_type(self.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        super(CollectionSite, self).clean()
