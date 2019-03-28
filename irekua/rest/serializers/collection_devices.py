# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import physical_devices
from . import data_collections


class SelectSerializer(data_collections.CollectionSerializer):
    device = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.CollectionDevice.objects.all(),
        source='id')

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'device'
        )

    def update_querysets(self):
        if self.collection is not None:
            self.fields['device'].queryset = (
                db.CollectionDevice.objects.filter(
                    collection=self.collection
                )
            )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    device = physical_devices.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'device',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device = physical_devices.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'device',
            'internal_id',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'serial_number',
            'device',
            'metadata',
            'bundle',
        )
