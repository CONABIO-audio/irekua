# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    device_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='device_type-detail')
    brand = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='device_brand-detail')
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')
    configuration_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

    class Meta:
        model = db.Device
        fields = (
            'url',
            'device_type',
            'brand',
            'model',
            'configuration_schema',
        )
