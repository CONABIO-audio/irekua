# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import physical_devices


class SelectSerializer(serializers.ModelSerializer):
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


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'id',
            'internal_id',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    physical_device = physical_devices.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'physical_device',
            'internal_id',
            'metadata',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'physical_device',
            'metadata',
            'internal_id',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)
