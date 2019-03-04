from django.contrib.postgres.fields import JSONField
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from database.utils import (
    validate_coordinates_and_geometry,
    validate_json_instance,
    empty_json,
    GENERIC_SITE,
)


class Site(models.Model):
    name = models.CharField(
        max_length=70,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site'),
        blank=True)
    site_type = models.ForeignKey(
        'SiteType',
        on_delete=models.PROTECT,
        db_column='site_type',
        verbose_name=_('site type'),
        help_text=_('Type of site'),
        default=GENERIC_SITE,
        blank=False,
        null=False)
    geo_ref = PointField(
        blank=True,
        db_column='geo_ref',
        verbose_name=_('geo ref'),
        help_text=_('Georeference of site as Geometry'),
        spatial_index=True)
    latitude = models.FloatField(
        db_column='latitude',
        verbose_name=_('latitude'),
        help_text=_('Latitude of site'),
        blank=True)
    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of site'),
        blank=True)
    altitude = models.FloatField(
        blank=True,
        db_column='altitude',
        verbose_name=_('altitude'),
        help_text=_('Altitude of site (in meters)'),
        null=True)
    metadata = JSONField(
        db_column='metadata',
        verbose_name=_('metadata'),
        help_text=_('Metadata associated to site'),
        default=empty_json,
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

    def sync_coordinates_and_georef(self):
        if self.geo_ref and self.latitude and self.longitude:
            validate_coordinates_and_geometry(
                self.geo_ref,
                self.latitude,
                self.longitude)
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
            return

        if self.latitude and self.longitude:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        msg = _('Geo reference or longitude-latitude must be provided')
        raise forms.ValidationError(msg)

    def __str__(self):
        if self.name != '':
            return self.name
        return _('Site {id}').format(id=self.id)

    def clean(self, *args, **kwargs):
        self.sync_coordinates_and_georef()
        validate_json_instance(
            self.metadata,
            self.site_type.metadata_schema.schema)
        super(Site, self).clean(*args, **kwargs)
