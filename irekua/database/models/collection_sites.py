from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
        verbose_name = _('Collection Site')
        verbose_name_plural = _('Collection Sites')

        unique_together = (
            ('collection', 'internal_id'),
        )

    def __str__(self):
        msg = _('Site %(site)s of collection %(collection)')
        params = dict(
            site=str(self.site),
            collection=str(self.collection))
        return msg % params

    def clean(self):
        try:
            self.collection.validate_and_get_site_type(
                self.site.site_type)
        except ValidationError as error:
            raise ValidationError({'site': error})

        super(CollectionSite, self).clean()
