from django.db import models
from django.utils.translation import gettext_lazy as _

from database.models.schemas import Schema


class SiteType(models.Model):
    name = models.CharField(
        max_length=128,
        primary_key=True,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site type'),
        blank=False)
    description = models.TextField(
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of site type'),
        blank=False)
    metadata_schema = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for site metadata'),
        limit_choices_to={'field': Schema.SITE_METADATA},
        blank=False,
        null=False)

    class Meta:
        verbose_name = _('Site Type')
        verbose_name_plural = _('Site Types')

    def __str__(self):
        return self.name

    def validate_metadata(self, metadata):
        try:
            self.metadata_schema.validate_instance(metadata)
        except ValidationError as error:
            msg = _('Invalid site metadata for site of type %(type)s. Error: %(error)')
            params = dict(type=str(self), error=str(error))
            raise ValidationError(msg, params=params)
