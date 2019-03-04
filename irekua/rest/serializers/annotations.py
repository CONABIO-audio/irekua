# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Annotation
        fields = (
            'item',
            'event_type',
            'label_type',
            'label',
            'annotation_type',
            'annotation',
            'metadata_type',
            'metadata',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'model',
            'created_by'
            'last_modified_by',
        )
