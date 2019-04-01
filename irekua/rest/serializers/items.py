# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Item
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    item_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True)
    collection = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name',
        source='sampling_event.collection')

    class Meta:
        model = db.Item
        fields = (
            'url',
            'item_type',
            'captured_on',
            'collection',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Item
        fields = (
            'url',
            'id',
            'hash',
            'item_type',
            'media_info',
            'metadata',
            'sampling_event',
            'captured_on',
            'licence',
            'tags',
            'ready_event_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Item
        fields = (
            'hash',
            'item_file',
            'item_type',
            'media_info',
            'metadata',
            'captured_on',
            'licence',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        licences = self.fields['licence']
        item_types = self.fields['item_type']

        try:
            sampling_event = self.context['sampling_event']
            collection = sampling_event.collection
            collection_type = collection.collection_type

            licences.queryset = collection.licence_set

            if collection_type.restrict_item_types:
                item_types.queryset = (
                    collection_type.item_types.all()
                )

        except (KeyError, AttributeError):
            pass

    def create(self, validated_data):
        sampling_event = self.context['sampling_event']
        validated_data['sampling_event'] = sampling_event
        return super().create(validated_data)


class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Item
        fields = (
            'item_file',
        )
