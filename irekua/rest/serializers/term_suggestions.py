# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSuggestionSerializer(serializers.ModelSerializer):
    term_type_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:termtype-detail',
        source='term_type')
    suggested_by_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:user-detail')
    suggested_by = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.TermSuggestion
        fields = (
            'url',
            'term_type',
            'term_type_url',
            'value',
            'description',
            'metadata',
            'suggested_by',
            'suggested_by_url',
            'suggested_on',
        )
        extra_kwargs = {
            'suggested_on': {'read_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        term_suggestion = db.TermSuggestion.objects.create(
            suggested_by=user,
            **validated_data)
        return term_suggestion

    def update(self, instance, validated_data):
        instance.value = validated_data['value']
        instance.description = validated_data['description']
        instance.metadata = validated_data['metadata']
        instance.save()
        return instance
