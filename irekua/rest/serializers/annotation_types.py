# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
            'description',
            'annotation_schema',
            'icon'
        )
