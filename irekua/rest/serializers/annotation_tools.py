# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db

from .schemas import SchemaSerializer


class AnnotationToolSerializer(serializers.HyperlinkedModelSerializer):
    configuration_schema = SchemaSerializer(many=False, read_only=True)

    class Meta:
        model = db.AnnotationTool
        fields = (
            'url',
            'name',
            'version',
            'description',
            'logo',
            'url',
            'configuration_schema'
        )
