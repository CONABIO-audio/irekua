from django.db import models
from django.contrib.gis.db.models import MultiPolygonField
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON


class Locality(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        help_text=_('Name of locality'),
        blank=False)
    description = models.TextField(
        blank=True,
        db_column='description',
        verbose_name=_('description'),
        help_text=_('Description of the locality'))
    locality_type = models.ForeignKey(
        'LocalityType',
        on_delete=models.PROTECT,
        db_column='locality_type_id',
        verbose_name=_('locality type'),
        help_text=_('Type of locality'),
        blank=False,
        null=False)
    geometry = MultiPolygonField(
        blank=True,
        db_column='geometry',
        verbose_name=_('geometry'),
        help_text=_('Geometry of locality'),
        spatial_index=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to locality'),
        default=empty_JSON,
        blank=True,
        null=True)

    is_part_of = models.ManyToManyField(
        "self",
        symmetrical=False)

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')

        ordering = ['-name']
