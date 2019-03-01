# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EntailmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Entailment
        fields = (
            'url',
            'source',
            'target',
            'metadata_type',
            'metadata',
        )
