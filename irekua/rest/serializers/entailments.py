# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'url',
            'term_type',
            'value'
        )


class EntailmentSerializer(serializers.ModelSerializer):
    source_info = TermSerializer(
        many=False,
        read_only=True,
        source='source')
    target_info = TermSerializer(
        many=False,
        read_only=True,
        source='target')

    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'source',
            'source_info',
            'target',
            'target_info',
            'metadata',
        )

        extra_kwargs = {
            'source': {'write_only': True},
            'target': {'write_only': True},
        }
