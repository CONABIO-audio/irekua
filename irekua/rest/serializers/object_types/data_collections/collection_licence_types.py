# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import LicenceType

from rest.serializers.object_types import licence_types
from . import collection_types


MODEL = CollectionType.licence_types.through


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    licence_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='licencetype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'licence_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    licence_type = licence_types.SelectSerializer(
        many=False,
        read_only=True,
        source='licencetype')
    collection_type = collection_types.SelectSerializer(
        many=False,
        read_only=True,
        source='collectiontype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'collection_type',
            'licence_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    licence_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=LicenceType.objects.all(),
        source='licencetype')

    class Meta:
        model = MODEL
        fields = (
            'licence_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
