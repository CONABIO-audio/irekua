# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class PhysicalDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'device',
            'owner',
            'metadata_type',
            'metadata',
            'bundle',
        )
