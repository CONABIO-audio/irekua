# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.DeviceType.objects.all())

    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceType
        fields = (
            'name',
            'description',
            'icon',
        )
