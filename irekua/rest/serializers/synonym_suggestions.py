# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'url',
            'term_type',
            'value'
        )


class SynonymSuggestionSerializer(serializers.ModelSerializer):
    source_info = TermSerializer(many=False, read_only=True, source='source')
    suggested_by_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail',
        source='suggested_by')
    suggested_by = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'source',
            'source_info',
            'synonym',
            'description',
            'metadata',
            'suggested_by',
            'suggested_by_url',
            'suggested_on',
        )
        extra_kwargs = {
            'suggested_on': {'read_only': True},
            'source': {'write_only': True}
        }

    def create(self, validated_data):
        user = self.context['request'].user
        term_suggestion = db.SynonymSuggestion.objects.create(
            suggested_by=user,
            **validated_data)
        return term_suggestion

    def update(self, instance, validated_data):
        instance.synonym = validated_data['synonym']
        instance.description = validated_data['description']
        instance.metadata = validated_data['metadata']
        instance.save()
        return instance
