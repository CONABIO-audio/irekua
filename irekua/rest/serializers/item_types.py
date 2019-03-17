# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
        )


class ItemTypeSerializer(serializers.ModelSerializer):
    event_types = EventTypeSerializer(
        many=True,
        read_only=True)

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
