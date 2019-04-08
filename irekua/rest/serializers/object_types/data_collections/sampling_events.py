# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import SamplingEventType

from rest.serializers.object_types.sampling_events import sampling_event_types
from . import collection_types


MODEL = CollectionType.sampling_event_types.through


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'sampling_event_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    sampling_event_type = sampling_event_types.SelectSerializer(
        many=False,
        read_only=True,
        source='samplingeventtype')
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
            'sampling_event_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    sampling_event_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SamplingEventType.objects.all(),
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'sampling_event_type',
        )

    def create(self, validated_data):
        collection_type = self.context['collection_type']
        validated_data['collectiontype'] = collection_type
        return super().create(validated_data)
