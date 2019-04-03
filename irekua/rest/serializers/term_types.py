# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import TermType


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TermType
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
        model = TermType
        fields = (
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
        )
