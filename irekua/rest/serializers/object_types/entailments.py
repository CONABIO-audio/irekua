# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import EntailmentType

from rest.serializers.object_types import term_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntailmentType


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'url',
            'id',
            'source_type',
            'target_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    source_type = term_types.SelectSerializer(many=False, read_only=True)
    target_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = EntailmentType
        fields = (
            'url',
            'id',
            'source_type',
            'target_type',
            'metadata_schema',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'source_type',
            'target_type',
            'metadata_schema',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntailmentType
        fields = (
            'metadata_schema',
        )
