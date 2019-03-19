# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db

from . import device_brands
from . import device_types


class SelectSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Device.objects.all())

    class Meta:
        model = db.Device
        fields = (
            'url',
            'device',
        )


class DetailSerializer(serializers.ModelSerializer):
    device_type = device_types.ListSerializer(
        many=False,
        read_only=True)
    brand = device_brands.ListSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.Device
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


class ListSerializer(serializers.ModelSerializer):
    device_type = device_types.ListSerializer(
        many=False,
        read_only=True)
    brand = device_brands.ListSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.Device
        fields = (
            'url',
            'device_type',
            'brand',
            'model',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'device_type',
            'brand',
            'model',
            'metadata_schema',
            'configuration_schema',
        )
