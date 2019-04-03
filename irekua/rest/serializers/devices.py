# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Device

from . import device_brands
from . import device_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_type = device_types.SelectSerializer(
        many=False,
        read_only=True)
    brand = device_brands.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = Device
        fields = (
            'url',
            'id',
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
        )
