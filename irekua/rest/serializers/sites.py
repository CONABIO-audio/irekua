# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Site
from database.models import SamplingEvent
from database.models import SamplingEventDevice
from database.models import CollectionSite
from database.models import Item

from rest.serializers.object_types import sites
from rest.serializers.users import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'site_type',
            'name',
            'locality',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = sites.SelectSerializer(many=False, read_only=True)
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'metadata',
            'created_by',
            'created_on',
            'modified_on',
        )


class FullDetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = sites.SelectSerializer(many=False, read_only=True)
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'latitude',
            'longitude',
            'geo_ref',
            'altitude',
            'metadata',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
            'site_type',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
            'site_type',
            'altitude',
            'metadata',
        )


class GeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'latitude',
            'longitude',
            'altitude',
            'geo_ref',
        )


class SiteLocationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(read_only=True, source="*")

    class Meta:
        model = Site
        fields = (
            'id',
            'geometry'
        )

class SamplingEventLocationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="collection_site.site")

    class Meta:
        model = SamplingEvent
        fields = (
            'id',
            'geometry'
        )

class SamplingEventDeviceLocationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="sampling_event.collection_site.site")

    class Meta:
        model = SamplingEventDevice
        fields = (
            'id',
            'geometry'
        )


class ItemLocationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="sampling_event_device.sampling_event.collection_site.site")

    class Meta:
        model = Item
        fields = (
            'id',
            'geometry'
        )

class CollectionSiteLocationSerializer(serializers.ModelSerializer):
    geometry = GeometrySerializer(
        read_only=True,
        source="site")

    class Meta:
        model = CollectionSite
        fields = (
            'id',
            'geometry'
        )
