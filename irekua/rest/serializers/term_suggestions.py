# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    term_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term_type-detail')
    suggested_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.TermSuggestion
        fields = (
            'url',
            'term_type',
            'value',
            'description',
            'metadata',
            'suggested_by',
            'suggested_on',
        )
