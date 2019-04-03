# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEventType

from . import device_types
from . import site_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name'
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'icon',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_types = device_types.SelectSerializer(
        many=True,
        read_only=True)
    site_types = site_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = SamplingEventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
            'device_types',
            'site_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventType
        fields = (
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
        )
