# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionDeviceSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='physical_device-detail')
    collection = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection-detail')

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'device',
            'collection',
            'internal_id',
            'metadata'
        )
