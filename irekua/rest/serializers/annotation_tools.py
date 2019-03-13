# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationToolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.AnnotationTool
        fields = (
            'url',
            'id',
            'name',
            'version',
            'description',
            'logo',
            'website',
            'configuration_schema'
        )
