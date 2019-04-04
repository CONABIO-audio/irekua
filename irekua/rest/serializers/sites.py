# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Site

from . import site_types
from . import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'site_type',
            'name',
            'locality',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.SelectSerializer(many=False, read_only=True)
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'metadata',
            'created_by',
            'created_on',
            'modified_on',
        )


class FullDetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.SelectSerializer(many=False, read_only=True)
    created_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'latitude',
            'longitude',
            'geo_ref',
            'altitude',
            'metadata',
            'created_by',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = (
            'name',
            'locality',
            'site_type',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
