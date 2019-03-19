# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import terms


class ListSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)
    target = terms.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'source',
            'target',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    source = terms.ListSerializer(many=False, read_only=True)
    target = terms.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'id',
            'source',
            'target',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Entailment
        fields = (
            'source',
            'target',
            'metadata',
        )
