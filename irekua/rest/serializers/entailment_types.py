# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EntailmentTypeSerializer(serializers.ModelSerializer):
    source_type_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name='termtype-detail',
        source='source_type')
    target_type_url = serializers.HyperlinkedRelatedField(
        read_only=True,
        many=False,
        view_name='termtype-detail',
        source='target_type')

    class Meta:
        model = db.EntailmentType
        fields = (
            'url',
            'id',
            'source_type',
            'target_type',
            'source_type_url',
            'target_type_url',
            'metadata_schema',
        )

    def create(self, validated_data):
        target_type = db.TermType.objects.get(pk=validated_data.pop('target_type'))
        source_type = db.TermType.objects.get(pk=validated_data.pop('source_type'))

        entailment_type = db.EntailmentType.objects.create(
            target_type=target_type,
            source_type=source_type,
            **validated_data)

        return entailment_type
