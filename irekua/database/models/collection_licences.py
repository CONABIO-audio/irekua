from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CollectionLicence(models.Model):
    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE,
        db_column='collection_id',
        verbose_name=_('collection'),
        help_text=_('Collection in which licence is valid'),
        blank=False,
        null=False)
    licence = models.ForeignKey(
        'Licence',
        on_delete=models.PROTECT,
        db_column='licence_id',
        verbose_name=_('licence'),
        help_text=_('Licence which forms part of collection'),
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Collection Licence')
        verbose_name_plural = _('Collection Licences')

    def __str__(self):
        msg = _('Licence %(licence)s is part of collection %(collection)s')
        params = dict(
            licence=str(self.licence),
            collection=str(self.collection))
        return msg % params

    def clean(self):
        try:
            self.collection.validate_and_get_licence_type(
                self.licence.licence_type)
        except ValidationError as error:
            raise ValidationError({'licence': error})
        super(CollectionLicence, self).clean()
