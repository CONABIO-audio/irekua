# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ListDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'device_type',
            'brand',
            'model')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Device
        fields = (
            'url',
            'device_type',
            'brand',
            'model')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.User
        fields = (
            'url',
            'username')


class ListSerializer(serializers.HyperlinkedModelSerializer):
    device = ListDeviceSerializer(many=False, read_only=True)

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'device'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device = DeviceSerializer(many=False, read_only=True)
    owner = UserSerializer(many=False, read_only=True)

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'owner',
            'metadata',
            'bundle',
            'device',
        )

class CreateSerializer(serializers.HyperlinkedModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Device.objects.all())

    class Meta:
        model = db.PhysicalDevice
        fields = (
            'url',
            'serial_number',
            'device',
            'metadata',
            'bundle',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return db.PhysicalDevice.objects.create(**validated_data)
