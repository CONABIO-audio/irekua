# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db

from .schemas import SchemaSerializer


class AnnotationTypeSerializer(serializers.HyperlinkedModelSerializer):
    schema = SchemaSerializer(many=False, read_only=True)

    class Meta:
        model = db.AnnotationType
        fields = (
                'url',
                'name',
                'description',
                'schema')
