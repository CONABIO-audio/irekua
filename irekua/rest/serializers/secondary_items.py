# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SecondaryItemSerializer(serializers.HyperlinkedModelSerializer):
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
