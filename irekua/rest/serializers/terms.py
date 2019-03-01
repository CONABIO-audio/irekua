# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class TermSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Term
        fields = (
            'url',
            'term_type',
            'value',
            'description',
            'metadata_type',
            'metadata'
        )
