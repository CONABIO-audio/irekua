# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionDeviceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'device',
            'collection',
            'internal_id',
            'metadata_type',
            'metadata',
        )
