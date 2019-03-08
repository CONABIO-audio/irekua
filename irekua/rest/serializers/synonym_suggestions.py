# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SynonymSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term-detail')
    suggested_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'source',
            'synonym',
            'description',
            'metadata',
            'suggested_by',
            'suggested_on',
        )
