# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class EventTypeSerializer(serializers.HyperlinkedModelSerializer):
    label_term_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='term_type-detail')

    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'label_term_types')
