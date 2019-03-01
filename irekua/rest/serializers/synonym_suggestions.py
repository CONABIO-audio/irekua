# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SynonymSuggestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'source',
            'synonym',
            'description',
            'metadata_type',
            'metadata',
            'suggested_by',
            'suggested_on',
        )
