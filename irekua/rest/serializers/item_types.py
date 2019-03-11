# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ItemTypeSerializer(serializers.HyperlinkedModelSerializer):
    event_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='event_type-detail')

    class Meta:
        model = db.ItemType
        fields = (
            'url',
            'name',
            'description',
            'media_info_schema',
            'media_type',
            'icon',
            'event_types',
        )
