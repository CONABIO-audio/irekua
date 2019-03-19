# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SiteType.objects.all())

    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SiteType
        fields = (
            'name',
            'description',
            'metadata_schema'
        )
