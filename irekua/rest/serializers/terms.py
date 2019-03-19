# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import term_types


class ListSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.Term
        fields = (
            'url',
            'term_type',
            'value',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.Term
        fields = (
            'url',
            'id',
            'term_type',
            'value',
            'description',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'term_type',
            'value',
            'description',
            'metadata'
        )
