# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionItemTypeSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection_type-detail')
    item_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='item_type-detail')

    class Meta:
        model = db.CollectionItemType
        fields = (
            'url',
            'collection_type',
            'item_type',
            'metadata_schema',
        )
