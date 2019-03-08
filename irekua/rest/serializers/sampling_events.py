# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SamplingEventSerializer(serializers.HyperlinkedModelSerializer):
    sampling_event_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='sampling_event_type-detail')
    device = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='physical_device-detail')
    site = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='site-detail')

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event_type',
            'site'
            'device',
            'configuration',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        )
