# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationTypeSerializer(serializers.HyperlinkedModelSerializer):
    schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
            'description',
            'schema',
            'icon'
        )
