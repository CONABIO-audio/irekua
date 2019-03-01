# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ItemSerializer(serializers.HyperlinkedModelSerializer):
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
            'sampling',
            'source',
            'metadata_type',
            'metadata',
            'captured_on',
            'created_on',
            'collection',
            'owner',
            'licence',
            'is_uploaded')
