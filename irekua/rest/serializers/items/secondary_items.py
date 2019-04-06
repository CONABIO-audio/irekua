# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SecondaryItem

from rest.serializers.object_types import item_types
from . import items


class SelectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
            'item',
            'item_type'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    item_type = item_types.SelectSerializer(many=False, read_only=True)
    item = items.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = SecondaryItem
        fields = (
            'url',
            'id',
            'hash',
            'path',
            'item_type',
            'item',
            'media_info',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryItem
        fields = (
            'hash',
            'path',
            'item_type',
            'item',
            'media_info',
        )

    def create(self, validated_data):
        item = self.context['item']
        validated_data['item'] = item
        return super().create(validated_data)
