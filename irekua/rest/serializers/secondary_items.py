# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SecondaryItemSerializer(serializers.HyperlinkedModelSerializer):
    item = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='item-detail')
    item_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='item_type-detail')

    class Meta:
        model = db.SecondaryItem
        fields = (
            'url',
            'path',
            'hash',
            'hash_function',
            'created_on',
            'item_type',
            'item',
            'media_info'
        )
