# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEvent

from . import sites
from . import physical_devices
from . import users
from . import sampling_event_types
from . import data_collections
from . import licences


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    site = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name')
    site_id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='site')
    device_type = serializers.CharField(
        read_only=True,
        source='physical_device.device.device_type.name')

    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'site',
            'site_id',
            'device_type',
            'started_on',
            'ended_on',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event_type = sampling_event_types.SelectSerializer(
        many=False,
        read_only=True)
    collection = data_collections.SelectSerializer(
        many=False,
        read_only=True)
    licence = licences.SelectSerializer(
        many=False,
        read_only=True)
    physical_device = physical_devices.SelectSerializer(
        many=False,
        read_only=True)
    site = sites.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'site',
            'physical_device',
            'configuration',
            'commentaries',
            'metadata',
            'collection',
            'licence',
            'started_on',
            'ended_on',
            'created_by',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = (
            'sampling_event_type',
            'site',
            'physical_device',
            'configuration',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
            'licence',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            collection = self.context['collection']

            sites_field = self.fields['site']
            sites_field.queryset = collection.sites.all()

            physical_devices_field = self.fields['physical_device']
            physical_devices_field.queryset = collection.physical_devices.all()

            licences_field = self.fields['licence']
            licences_field.queryset = collection.licence_set.all()

        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        collection = self.context['collection']

        validated_data['created_by'] = user
        validated_data['collection'] = collection
        return super().create(validated_data)
