# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import devices
from . import users


class SelectSerializer(serializers.ModelSerializer):
    physical_device = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.PhysicalDevice.objects.all(),
        source='id')

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'physical_device'
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    device = devices.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'device'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device = devices.DetailSerializer(many=False, read_only=True)
    owner = users.SelectSerializer(many=False, read_only=True)

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'owner',
            'metadata',
            'bundle',
            'device',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.PhysicalDevice
        fields = (
            'serial_number',
            'device',
            'metadata',
            'bundle',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return db.PhysicalDevice.objects.create(**validated_data)
