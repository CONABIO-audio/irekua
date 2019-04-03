# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Term

from . import term_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        models = Term
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = (
            'url',
            'term_type',
            'value',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = Term
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
        model = Term
        fields = (
            'value',
            'description',
            'metadata'
        )

    def create(self, validated_data):
        validated_data['term_type'] = self.context['term_type']
        return super().create(validated_data)
