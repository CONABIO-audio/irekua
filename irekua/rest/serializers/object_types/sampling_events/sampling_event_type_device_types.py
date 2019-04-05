# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEventTypeDeviceType

from rest.serializers.object_types import device_types
from . import sampling_event_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id'
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'device_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_type = device_types.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event_type = sampling_event_types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'device_type',
            'metadata_schema',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'device_type',
            'metadata_schema',
        )

    def create(self, validated_data):
        sampling_event_type = self.context['sampling_event_type']
        validated_data['sampling_event_type'] = sampling_event_type
        return super().create(validated_data)


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeDeviceType
        fields = (
            'metadata_schema',
        )
