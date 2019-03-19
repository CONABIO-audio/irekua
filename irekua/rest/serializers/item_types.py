# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

import database.models as db
from . import event_types


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.ItemType.objects.all())

    class Meta:
        model = db.ItemType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.ItemType
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
        model = db.ItemType
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
        model = db.ItemType
        fields = (
            'name',
            'description',
            'media_info_schema',
            'media_type',
            'icon',
        )
