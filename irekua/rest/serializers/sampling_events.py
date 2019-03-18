# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ListDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'device_type',
            'brand',
            'model')

class ListSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Site
        fields = (
            'name',
            'site_type'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    site = ListSiteSerializer(many=False, read_only=True)
    device = ListDeviceSerializer(many=False, read_only=True)

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
            'started_on',
            'ended_on',
        )


class CreateSerializer(serializers.HyperlinkedRelatedField):
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
            'started_on',
            'ended_on',
        )
