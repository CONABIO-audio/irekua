# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'url',
            'name',
            'logo'
        )


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name',
        )


class DeviceSerializer(serializers.ModelSerializer):
    device_type_info = DeviceTypeSerializer(
        many=False,
        read_only=True,
        source='device_type')
    brand_info = BrandSerializer(
        many=False,
        read_only=True,
        source='brand')

    class Meta:
        model = db.Device
        fields = (
            'url',
            'id',
            'device_type',
            'device_type_info',
            'brand',
            'brand_info',
            'model',
            'metadata_schema',
            'configuration_schema',
        )
        extra_kwargs = {
            'device_type': {'write_only': True},
            'brand': {'write_only': True},
        }
