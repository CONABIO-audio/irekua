# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SiteSerializer(serializers.ModelSerializer):
    site_type_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:sitetype-detail',
        source='site_type')
    creator_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:user-detail',
        source='creator')
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'site_type_url',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
            'creator',
            'creator_url'
        )
        extra_kwargs = {
            'latitude': {'write_only': True},
            'longitude': {'write_only': True},
        }

    def create(self, validated_data):
        site_type = db.SiteType.objects.get(
            name=validated_data.pop('site_type'))
        user = self.context['request'].user
        validated_data['creator'] = user
        return db.Site.objects.create(site_type=site_type, **validated_data)


class FullSiteSerializer(serializers.ModelSerializer):
    site_type_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:sitetype-detail',
        source='site_type')
    creator_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:user-detail',
        source='creator')
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'site_type_url',
            'latitude',
            'longitude',
            'geo_ref',
            'altitude',
            'metadata',
            'creator',
            'creator_url'
        )
        extra_kwargs = {'geo_ref': {'read_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creator'] = user
        return db.Site.objects.create(**validated_data)
