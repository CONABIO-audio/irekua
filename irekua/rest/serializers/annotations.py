# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Annotation
        fields = (
            'item',
            'annotation_type',
            'event_type',
            'label',
            'annotation',
            'metadata',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'model',
            'created_by')
