# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import term_types
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.EventType.objects.all())

    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_types = term_types.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'term_types',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.EventType
        fields = (
            'name',
            'description',
            'icon',
        )
