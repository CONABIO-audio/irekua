# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermTypeSerializer(serializers.HyperlinkedModelSerializer):
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')
    synonym_metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

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
        )
