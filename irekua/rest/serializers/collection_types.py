# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionTypeSerializer(serializers.HyperlinkedModelSerializer):
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')
    site_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='site_type-detail')
    annotation_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='annotation_type-detail')
    licence_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='licence_type-detail')
    event_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='site_type-detail')
    sampling_event_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='sampling_event_type-detail')
    item_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='item_type-detail')
    device_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='device_type-detail')
    roles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='role-detail')

    class Meta:
        model = db.CollectionType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'administrators',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'site_types',
            'annotation_types',
            'licence_types',
            'event_types',
            'sampling_event_types',
            'item_types',
            'device_types',
            'roles'
        )
