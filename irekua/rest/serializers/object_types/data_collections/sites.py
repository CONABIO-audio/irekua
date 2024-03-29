# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import SiteType

from rest.serializers.object_types import sites
from . import types


MODEL = CollectionType.site_types.through  # pylint: disable=E1101


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'site_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = sites.SelectSerializer(
        many=False,
        read_only=True,
        source='sitetype')
    collection_type = types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'site_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SiteType.objects.all(),  # pylint: disable=E1101
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'site_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
