# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import sites
from . import physical_devices
from . import users
from . import sampling_event_types
from . import data_collections
from . import licences


class SelectSerializer(serializers.ModelSerializer):
    sampling_event = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SamplingEvent.objects.all())

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    site = sites.ListSerializer(many=False, read_only=True)
    device = physical_devices.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event_type',
            'site',
            'device',
            'started_on',
            'ended_on',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by = users.ListSerializer(
        many=False,
        read_only=True)
    sampling_event_type = sampling_event_types.ListSerializer(
        many=False,
        read_only=True)
    collection = data_collections.ListSerializer(
        many=False,
        read_only=True)
    licence = licences.DetailSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event_type',
            'site',
            'device',
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
        model = db.SamplingEvent
        fields = (
            'sampling_event_type',
            'site',
            'device',
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
            sites = self.fields['site']
            devices = self.fields['device']
            licences = self.fields['licence']

            sites.queryset = collection.sites.all()
            devices.queryset = collection.devices.all()
            licences.queryset = collection.licence_set.all()
        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        collection = self.context['collection']

        validated_data['created_by'] = user
        validated_data['collection'] = collection
        return super().create(validated_data)
