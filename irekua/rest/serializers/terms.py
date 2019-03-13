# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSerializer(serializers.ModelSerializer):
    term_type_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:termtype-detail',
        source='term_type')

    class Meta:
        model = db.Term
        fields = (
            'url',
            'term_type',
            'term_type_url',
            'value',
            'description',
            'metadata'
        )

    def create(self, validated_data):
        term_type = db.TermType.objects.get(name=validated_data.pop('term_type'))
        term = db.Term.objects.create(
            term_type=term_type,
            **validated_data)
        return term
