# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'url',
            'id',
            'term_type',
            'value'
        )
        extra_kwargs = {
            'term_type': {'read_only': True},
            'value': {'read_only': True},
        }


class SynonymSerializer(serializers.ModelSerializer):
    source = TermSerializer(many=False, read_only=False)
    target = TermSerializer(many=False, read_only=False)

    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'source',
            'target',
            'metadata'
        )
