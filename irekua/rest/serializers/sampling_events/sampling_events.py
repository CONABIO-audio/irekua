# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEvent

from rest.serializers.data_collections import sites
from rest.serializers.users import users
from rest.serializers.object_types.sampling_events import types
from rest.serializers.data_collections import data_collections
from rest.serializers import licences


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    collection_site = serializers.CharField(
        read_only=True,
        source='collection_site.site.name')
    site_internal_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='collection_site.internal_id')

    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'collection_site',
            'site_internal_id',
            'started_on',
            'ended_on',
        )


class UserListSerializer(serializers.ModelSerializer):
    collection_site = serializers.CharField(
        read_only=True,
        source='collection_site.site.name')
    site_internal_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='collection_site.internal_id')

    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
            'collection',
            'sampling_event_type',
            'collection_site',
            'site_internal_id',
            'started_on',
            'ended_on',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    created_by = users.SelectSerializer(
        many=False,
        read_only=True)
    modified_by = users.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event_type = types.SelectSerializer(
        many=False,
        read_only=True)
    collection = data_collections.SelectSerializer(
        many=False,
        read_only=True)
    licence = licences.SelectSerializer(
        many=False,
        read_only=True)
    collection_site = sites.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEvent
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'collection_site',
            'commentaries',
            'metadata',
            'collection',
            'licence',
            'started_on',
            'ended_on',
            'created_by',
            'modified_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = (
            'sampling_event_type',
            'collection_site',
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

            sites_field = self.fields['collection_site']
            sites_field.queryset = collection.collectionsite_set.all()

            licences_field = self.fields['licence']
            licences_field.queryset = collection.licence_set.all()

        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        collection = self.context['collection']

        validated_data['created_by'] = user
        validated_data['modified_by'] = user
        validated_data['collection'] = collection
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEvent
        fields = (
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        )

    def update(self, validated_data):
        user = self.context['request'].user
        validated_data['modified_by'] = user
        return super().update(validated_data)
