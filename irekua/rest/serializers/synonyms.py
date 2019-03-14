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


class SynonymSerializer(serializers.ModelSerializer):
    source_info = TermSerializer(
        many=False,
        read_only=True,
        label='Source of synonym',
        help_text='Source of synonym',
        source='source')
    target_info = TermSerializer(
        many=False,
        read_only=True,
        label='Target of Synonym',
        help_text='Target of synonym',
        source='target')

    queryset = db.Term.objects.all()
    source = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        label='source',
        queryset=queryset)
    target = serializers.PrimaryKeyRelatedField(
        many=False,
        write_only=True,
        label='target',
        queryset=queryset)

    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'metadata',
            'source',
            'target',
            'source_info',
            'target_info',
        )
