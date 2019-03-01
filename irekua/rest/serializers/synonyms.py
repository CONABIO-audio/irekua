# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SynonymSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Synonym
        fields = (
            'url',
            'source',
            'target',
            'metadata_type',
            'metadata'
        )
