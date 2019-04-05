# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionItemType

from rest.serializers.object_types import item_types
from . import collection_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
            'item_type',
            'metadata_schema',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    item_type = item_types.SelectSerializer(
        many=False,
        read_only=True)
    collection_type = collection_types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'id',
            'collection_type',
            'item_type',
            'metadata_schema',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItemType
        fields = (
            'item_type',
            'metadata_schema',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collection_type'] = collection_type
        return super().create(validated_data)
