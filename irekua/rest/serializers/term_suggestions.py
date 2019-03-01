# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.TermSuggestion
        fields = (
            'url',
            'term_type',
            'value',
            'description',
            'metadata_type',
            'metadata',
            'suggested_by',
            'suggested_on',
        )
