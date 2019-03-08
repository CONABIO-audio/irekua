# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class PhysicalDeviceSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='device-detail')
    owner = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'device',
            'owner',
            'metadata',
            'bundle',
        )
