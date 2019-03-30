# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import data_collections
from . import sites


class SelectSerializer(serializers.ModelSerializer):
    site = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.CollectionSite.objects.all(),
        source='id')

    class Meta:
        model = db.CollectionSite
        fields = (
            'url',
            'site'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    site = sites.ListSerializer(
        many=False,
        read_only=True)
    collection = sites.ListSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.CollectionSite
        fields = (
            'url',
            'site',
            'collection',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site = sites.DetailSerializer(
        many=False,
        read_only=True)
    collection = data_collections.ListSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.CollectionSite
        fields = (
            'url',
            'collection',
            'site',
            'internal_id',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.CollectionSite
        fields = (
            'site',
            'metadata',
        )
