# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import EventType

from rest.serializers.object_types import events
from . import types


MODEL = CollectionType.event_types.through  # pylint: disable=E1101


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='eventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'event_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    event_type = events.SelectSerializer(
        many=False,
        read_only=True,
        source='eventtype')
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
            'event_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=EventType.objects.all(),  # pylint: disable=E1101
        source='eventtype')

    class Meta:
        model = MODEL
        fields = (
            'event_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
