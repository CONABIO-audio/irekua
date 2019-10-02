from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON


class LocalityType(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        help_text=_('Name of locality'))
    description = models.TextField(
        blank=True,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of type of locality'))
    source = models.URLField(
        max_length=128,
        blank=True,
        db_column='source',
        verbose_name=_('source'),
        help_text=_('Source of information for localities of this type'))
    original_datum = models.TextField(
        blank=True,
        db_column='original_datum',
        verbose_name=_('original datum'),
        help_text=_(
            'Datum used for the original coordinates for localities'
            ' of this type in WTK format'))
    metadata_schema = JSONField(
        db_column='metadata_schema',
        verbose_name=_('metadata_schema'),
        help_text=_('JSON Schema for metadata of localities of this type'),
        default=empty_JSON,
        blank=True,
        null=True)
    publication_date = models.DateField(
        blank=True,
        db_column='publication_date',
        verbose_name=_('publication date'),
        help_text=_('Date of publication of localities defined in this type'))

    class Meta:
        verbose_name = _('Location Type')
        verbose_name_plural = _('Location Types')

        ordering = ['-name']
