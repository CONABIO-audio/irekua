# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import EventType

from . import term_types


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=EventType.objects.all())

    class Meta:
        model = EventType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
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
        model = EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'term_types',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'name',
            'description',
            'icon',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = (
            'description',
            'icon',
        )
