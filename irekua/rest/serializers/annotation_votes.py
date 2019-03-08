# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class AnnotationVoteSerializer(serializers.HyperlinkedModelSerializer):
    annotation = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='annotation-detail')
    created_by = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.AnnotationVote
        fields = (
            'url',
            'annotation',
            'label',
            'created_by',
            'created_on',
            'modified_on'
        )
