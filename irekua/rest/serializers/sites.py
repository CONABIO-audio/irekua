# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import site_types
from . import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Site
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Site
        fields = (
            'url',
            'name',
            'locality',
            'site_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.DetailSerializer(many=False, read_only=True)
    created_by = users.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'metadata',
            'created_by',
        )


class FullDetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.DetailSerializer(many=False, read_only=True)
    created_by = users.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Site
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
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Site
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
        site_type = db.SiteType.objects.get(
            name=validated_data.pop('site_type'))
        user = self.context['request'].user
        validated_data['created_by'] = user
        return db.Site.objects.create(site_type=site_type, **validated_data)
