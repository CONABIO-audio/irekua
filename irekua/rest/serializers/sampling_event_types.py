
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SamplingEventTypeSerializer(serializers.HyperlinkedModelSerializer):
    device_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='device_type-detail')
    site_types = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='site_type-detail')

    class Meta:
        model = db.SamplingEventType
        fields = (
            'url',
            'name',
            'description',
            'icon',
            'metadata_schema',
            'restrict_device_types',
            'restrict_site_types',
            'device_types',
            'site_types'
        )
