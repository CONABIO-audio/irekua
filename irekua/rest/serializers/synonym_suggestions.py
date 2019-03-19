# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import terms
from . import users


class SelectSerializer(serializers.ModelSerializer):
    suggestion = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SynonymSuggestion.objects.all(),
        source='id')

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'suggestion'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'source',
            'synonym',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)
    suggested_by = users.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'url',
            'id',
            'source',
            'synonym',
            'description',
            'metadata',
            'suggested_by',
            'suggested_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'source',
            'synonym',
            'description',
            'metadata',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['suggested_by'] = user
        return super().create(validated_data)
