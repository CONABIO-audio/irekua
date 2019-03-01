# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SchemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Schema
        fields = (
            'url',
            'field',
            'name',
            'description',
            'schema',
        )
