# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Item

from . import item_types
from . import sampling_events
from . import licences
from . import tags
from . import event_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = (
            'url',
            'id',
            'item_type',
            'captured_on',
            'collection',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    item_type = item_types.SelectSerializer(many=False, read_only=True)
    sampling_event = sampling_events.SelectSerializer(many=False, read_only=True)
    licence = licences.SelectSerializer(many=False, read_only=True)
    tags = tags.SelectSerializer(many=True, read_only=True)
    ready_event_types = event_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Item
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
        model = Item
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
        model = Item
        fields = (
            'item_file',
        )
