# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name')


class SiteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name')


class SamplingEventTypeSerializer(serializers.HyperlinkedModelSerializer):
    device_types = DeviceTypeSerializer(
        many=True,
        read_only=True)
    site_types = SiteTypeSerializer(
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
            'site_types'
        )
