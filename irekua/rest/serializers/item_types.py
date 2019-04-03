# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import ItemType

from . import event_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    event_types = event_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = ItemType
        fields = (
            'url',
            'name',
            'description',
            'media_info_schema',
            'media_type',
            'icon',
            'event_types',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemType
        fields = (
            'name',
            'description',
            'media_info_schema',
            'media_type',
            'icon',
        )
