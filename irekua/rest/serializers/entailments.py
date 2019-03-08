# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EntailmentSerializer(serializers.HyperlinkedModelSerializer):
    source = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term-detail')
    target = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='term-detail')


    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'source',
            'target',
            'metadata',
        )
