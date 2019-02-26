from django.contrib.postgres.fields import JSONField
from django.contrib.gis.db.models import PointField
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    name = models.CharField(
        max_length=70,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site'),
        blank=True)
    geo_ref = PointField(
        blank=False,
        db_column='geo_ref',
        verbose_name=_('geo ref'),
        help_text=_('Georeference of site as Geometry'),
        spatial_index=True)
    latitude = models.FloatField(
        db_column='latitude',
        verbose_name=_('latitude'),
        help_text=_('Latitude of site'),
        blank=False)
    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of site'),
        blank=False)
    altitude = models.FloatField(
        blank=True,
        db_column='altitude',
        verbose_name=_('altitude'),
        help_text=_('Altitude of site (in meters)'),
        null=True)
    metadata_type = models.ForeignKey(
        'Schema',
        on_delete=models.PROTECT,
        db_column='metadata_type',
        verbose_name=_('metadata type'),
        help_text=_('Schema for site metadata'),
        limit_choices_to=(
            models.Q(field__exact='site_metadata') |
            models.Q(field__exact='global')),
        to_field='name',
        default='free',
        blank=False,
        null=False)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to site'),
        blank=True,
        null=True)
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_column='creator_id',
        verbose_name=_('creator id'),
        help_text=_('Refrence to creator of site'))

    class Meta:
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')

    def __str__(self):
        if self.name != '':
            return self.name
        return _('Site {id}').format(id=self.id)
