# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from database.utils import simple_JSON_schema


class TermSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Term
        fields = ('url', 'value')


class TermTypeSerializer(serializers.HyperlinkedModelSerializer):
    term_set = TermSerializer(many=True, read_only=True)

    class Meta:
        model = db.TermType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'is_categorical',
            'metadata_schema',
            'synonym_metadata_schema',
            'term_set',
        )
