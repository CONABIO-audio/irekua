# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SecondaryItem
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    item_type = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name')

    class Meta:
        model = db.SecondaryItem
        fields = (
            'url',
            'item',
            'item_type'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SecondaryItem
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
        model = db.SecondaryItem
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
