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
        slug_field='name')

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
            'path',
            'item_type',
            'media_info',
            'metadata',
            'sampling_event',
            'captured_on',
            'collection',
            'owner',
            'licence',
            'tags',
            'ready_event_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.HyperlinkedModelSerializer):
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
