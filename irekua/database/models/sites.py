from django.contrib.postgres.fields import JSONField
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from database.utils import (
    empty_JSON,
    GENERIC_SITE,
)


def validate_coordinates_and_geometry(geometry, latitude, longitude):
    if geometry.x != longitude or geometry.y != latitude:
        msg = _('Georeference and longitude-latitude do not coincide')
        raise ValidationError(msg)


class Site(models.Model):
    name = models.CharField(
        max_length=128,
        db_column='name',
        verbose_name=_('name'),
        help_text=_('Name of site'),
        blank=True,
        null=True)
    locality = models.CharField(
        max_length=256,
        db_column='locality',
        verbose_name=_('locality'),
        help_text=_('Name of locality in which the site is located'),
        blank=True)
    site_type = models.ForeignKey(
        'SiteType',
        on_delete=models.PROTECT,
        db_column='site_type',
        verbose_name=_('site type'),
        help_text=_('Type of site'),
        to_field='name',
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
        default=empty_JSON,
        blank=True,
        null=True)
    creator = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        db_column='creator_id',
        verbose_name=_('creator'),
        help_text=_('Creator of site'))

    created_on = models.DateTimeField(
        db_column='created_on',
        verbose_name=_('created on'),
        help_text=_('Date of entry creation'),
        auto_now_add=True,
        editable=False)
    modified_on = models.DateTimeField(
        db_column='modified_on',
        verbose_name=_('modified on'),
        help_text=_('Date of last modification'),
        auto_now=True,
        editable=False)

    class Meta:
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')

        ordering = ['name']

        unique_together = (('name', 'site_type'))

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

        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        msg = _('Geo reference or longitude-latitude must be provided')
        raise ValidationError({'geo_ref': msg})

    def __str__(self):
        if self.name != '':
            return self.name
        return _('Site {id}').format(id=self.id)

    def clean(self):
        self.sync_coordinates_and_georef()

        try:
            self.site_type.validate_metadata(self.metadata)
        except ValidationError as error:
            raise ValidationError({'metadata': error})

        super(Site, self).clean()
