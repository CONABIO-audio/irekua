# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import TermSuggestion

from rest.serializers.object_types import term_types
from rest.serializers.users import users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermSuggestion
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermSuggestion
        fields = (
            'url',
            'id',
            'term_type',
            'value',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    term_type = term_types.SelectSerializer(many=False, read_only=True)
    suggested_by = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = TermSuggestion
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
        model = TermSuggestion
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


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermSuggestion
        fields = (
            'description',
            'metadata',
        )
