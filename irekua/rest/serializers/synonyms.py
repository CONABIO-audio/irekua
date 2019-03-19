# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import terms


class SelectSerializer(serializers.ModelSerializer):
    synonym = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Synonym.objects.all(),
        source='id')

    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'synonym'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)
    target = terms.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'source',
            'target',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.DetailSerializer(many=False, read_only=True)
    target = terms.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'metadata',
            'source',
            'target',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Synonym
        fields = (
            'metadata',
            'source',
            'target',
        )
