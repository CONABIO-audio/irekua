# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationToolSerializer(serializers.HyperlinkedModelSerializer):
    configuration_schema = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='schema-detail')

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
