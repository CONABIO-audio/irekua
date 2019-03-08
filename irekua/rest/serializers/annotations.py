# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationSerializer(serializers.HyperlinkedModelSerializer):
    annotation_tool = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='annotation_tool-detail')
    item = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='item-detail')
    event_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='event_type-detail')
    created_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')
    last_modified_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.Annotation
        fields = (
            'url',
            'annotation_tool',
            'item',
            'event_type',
            'label',
            'annotation_type',
            'annotation',
            'annotation_configuration',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'created_by',
            'last_modified_by',
        )
