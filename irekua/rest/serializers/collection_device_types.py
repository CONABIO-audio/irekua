# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionDeviceTypeSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection_type-detail')
    device_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='device_type-detail')
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

    class Meta:
        model = db.CollectionDeviceType
        fields = (
            'url',
            'collection_type',
            'device_type',
            'metadata_schema'
        )
