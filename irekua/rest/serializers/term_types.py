# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.TermType.objects.all())

    class Meta:
        model = db.TermType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
            'term_set',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.TermType
        fields = (
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
        )
