from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import PointField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.gis import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from database.models import CollectionUser
from database.models.base import IrekuaModelBaseUser
from database.utils import translate_doc
from database.models.items.items import Item
from database.models.sampling_events.sampling_events import SamplingEvent


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
        help_text=_('Name of site (visible only to owner)'),
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
        help_text=_('Latitude of site (in decimal degrees)'),
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        blank=True)
    longitude = models.FloatField(
        db_column='longitude',
        verbose_name=_('longitude'),
        help_text=_('Longitude of site (in decimal degrees)'),
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
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

        ordering = ['-created_on']

    def sync_coordinates_and_georef(self):
        if self.latitude is not None and self.longitude is not None:
            self.geo_ref = Point([self.longitude, self.latitude])
            return

        if self.geo_ref:
            self.latitude = self.geo_ref.y
            self.longitude = self.geo_ref.x
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

    @property
    def items(self):
        return Item.objects.filter(
            sampling_event_device__sampling_event__collection_site__site=self)

    @property
    def sampling_events(self):
        return SamplingEvent.objects.filter(
            collection_site__site=self)

    @property
    def map_widget(self):
        name = 'point_{}'.format(self.pk)
        widget = IrekuaMapWidget(attrs={
            'map_width': '100%',
            'map_height': '100%',
            'id': name,
            'disabled': True})

        return widget.render(name, self.geo_ref)

    @property
    def map_widget_no_controls(self):
        name = 'point_{}'.format(self.pk)
        widget = IrekuaMapWidgetNoControls(attrs={
            'map_width': '100%',
            'map_height': '100%',
            'id': name,
            'disabled': True})

        return widget.render(name, self.geo_ref)

    @property
    def map_widget_obscured(self):
        name = 'point_{}'.format(self.pk)
        widget = IrekuaMapWidgetObscured(attrs={
            'map_width': '100%',
            'map_height': '100%',
            'id': name,
            'disabled': True})

        return widget.render(name, self.geo_ref)



class IrekuaMapWidget(forms.OSMWidget):
    default_zoom = 12
    template_name = 'irekua/components/map_widget.html'


class IrekuaMapWidgetNoControls(forms.OSMWidget):
    default_zoom = 9
    template_name = 'irekua/components/map_widget_no_controls.html'


class IrekuaMapWidgetObscured(forms.OSMWidget):
    default_zoom = 12
    template_name = 'irekua/components/map_widget_obscured.html'
