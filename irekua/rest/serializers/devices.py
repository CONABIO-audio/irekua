# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'url',
            'device_type',
            'brand',
            'model',
        )
