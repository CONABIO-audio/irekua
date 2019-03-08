# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    item_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='item_type-detail')
    sampling_event = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='sampling_event-detail')
    source = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='source-detail')
    collection = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection-detail')
    owner = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')
    licence = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='licence-detail')
    tags = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='tag-detail')

    class Meta:
        model = db.Item
        fields = (
            'url',
            'path',
            'filesize',
            'hash',
            'hash_function',
            'item_type',
            'source_foreign_key',
            'media_info',
            'sampling_event',
            'source',
            'metadata_type',
            'metadata',
            'captured_on',
            'created_on',
            'collection',
            'owner',
            'licence',
            'is_uploaded',
            'tags')
