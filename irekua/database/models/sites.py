from django.contrib.postgres.fields import JSONField
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.utils import empty_JSON
from database.models import CollectionUser
from database.models.base import IrekuaModelBaseUser
from database.utils import translate_doc


@translate_doc
class Site(IrekuaModelBaseUser):
    help_text = _('''
        Site Model

        A site consists of the specification of coordinates. The datum assumed
        is WGS-84. A name for the site can be specified for easier future
        retrieval. Also an optional locality field is added to locate the site within a
        larger area and provide hierarchical organization of sites.

        The creator of the site is registered so that users can search within
        their previously created sites when setting up a new monitoring event.
    ''')

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

    class Meta:
        verbose_name = _('Site')
        verbose_name_plural = _('Sites')

        ordering = ['name']

    def sync_coordinates_and_georef(self):
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
        name = ''
        if self.name is not None:
            name = ': ' + self.name
        msg = _('Site %(id)s%(name)s')
        params = dict(
            id=self.id,
            name=name)
        return msg % params

    def clean(self):
        self.sync_coordinates_and_georef()
        super(Site, self).clean()

    def has_coordinate_permission(self, user):
        has_simple_permission = (
            user.is_superuser |
            user.is_model |
            user.is_curator |
            (self.created_by == user)
        )
        if has_simple_permission:
            return True

        collections = self.collection_set.all()

        for collection in collections.prefetch_related('collection_type'):
            collection_type = collection.collection_type
            queryset = collection_type.administrators.filter(id=user.id)
            if queryset.exists():
                return True

        collection_users = CollectionUser.objects.filter(
            user=user.pk,
            collection__in=collections)

        if not collection_users.exists():
            return False

        for collectionuser in collection_users.prefetch_related('role'):
            role = collectionuser.role
            queryset = role.permissions.filter(codename='view_collection_sites')
            if queryset.exists():
                return True

        return False
