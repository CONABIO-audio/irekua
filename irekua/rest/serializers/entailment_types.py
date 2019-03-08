# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EntailmentTypeSerializer(serializers.HyperlinkedModelSerializer):
    source_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term_type-detail')
    target_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term_type-detail')
    metadata_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')


    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'source_type',
            'target_type',
            'metadata_schema',
        )
