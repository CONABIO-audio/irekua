# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceTypeSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.DeviceType.objects.all())

    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name')


class SiteTypeSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.DeviceType.objects.all())

    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name')


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SamplingEventType
        fields = (
            'url',
            'name',
            'icon',
        )

class DetailSerializer(serializers.HyperlinkedModelSerializer):
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

class CreateSerializer(serializers.HyperlinkedModelSerializer):
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
        )
