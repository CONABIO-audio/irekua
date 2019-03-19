# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import sites
from . import physical_devices


class SelectSerializer(serializers.ModelSerializer):
    sampling_event = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SamplingEvent.objects.all())

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    site = sites.ListSerializer(many=False, read_only=True)
    device = physical_devices.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event_type',
            'site',
            'device',
            'started_on',
            'ended_on',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.SamplingEvent
        fields = (
            'url',
            'sampling_event_type',
            'site',
            'device',
            'configuration',
            'commentaries',
            'metadata',
            'collection',
            'licence',
            'started_on',
            'ended_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SamplingEvent
        fields = (
            'sampling_event_type',
            'site',
            'device',
            'configuration',
            'commentaries',
            'metadata',
            'started_on',
            'ended_on',
        )
