# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'type',
            'serial_number',
            'brand',
            'model',
            'owner',
            'metadata',
            'bundle')
