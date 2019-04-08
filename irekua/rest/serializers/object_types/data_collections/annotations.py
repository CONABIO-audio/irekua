# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import AnnotationType

from rest.serializers.object_types import annotations
from . import types


MODEL = CollectionType.annotation_types.through  # pylint: disable=E1101


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    annotation_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='annotationtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'annotation_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    annotation_type = annotations.SelectSerializer(
        many=False,
        read_only=True,
        source='annotationtype')
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
            'annotation_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    annotation_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=AnnotationType.objects.all(),  # pylint: disable=E1101
        source='annotationtype')

    class Meta:
        model = MODEL
        fields = (
            'annotation_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
