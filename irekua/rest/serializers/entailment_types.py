# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from . import term_types
import database.models as db


class ListSerializer(serializers.HyperlinkedModelSerializer):
    source_type = term_types.SelectSerializer(many=False, read_only=True)
    target_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.EntailmentType
        fields = (
            'url',
            'source_type',
            'target_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    source_type = term_types.SelectSerializer(many=False, read_only=True)
    target_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.EntailmentType
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
        model = db.EntailmentType
        fields = (
            'source_type',
            'target_type',
            'metadata_schema',
        )
