# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import device_types
from . import site_types


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SamplingEventType.objects.all())

    class Meta:
        model = db.SamplingEventType
        fields = (
            'url',
            'name'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SamplingEventType
        fields = (
            'url',
            'name',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_types = device_types.SelectSerializer(
        many=True,
        read_only=True)
    site_types = site_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = db.SamplingEventType
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
        model = db.SamplingEventType
        fields = (
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
        )
