# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import term_types
from . import users


class SelectSerializer(serializers.ModelSerializer):
    suggestion = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.TermSuggestion.objects.all(),
        source='id')

    class Meta:
        model = db.TermSuggestion
        fields = (
            'url',
            'suggestion',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.TermSuggestion
        fields = (
            'url',
            'term_type',
            'value',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.DetailSerializer(many=False, read_only=True)
    suggested_by = users.ListSerializer(many=False, read_only=True)

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


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.TermSuggestion
        fields = (
            'term_type',
            'value',
            'description',
            'metadata',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['suggested_by'] = user
        return super().create(validated_data)
