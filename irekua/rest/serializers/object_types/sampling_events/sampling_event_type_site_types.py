# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEventTypeSiteType

from rest.serializers.object_types import site_types
from . import sampling_event_types


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeSiteType
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeSiteType
        fields = (
            'url',
            'id',
            'site_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.SelectSerializer(
        many=False,
        read_only=True)
    sampling_event_type = sampling_event_types.SelectSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = SamplingEventTypeSiteType
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'site_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamplingEventTypeSiteType
        fields = (
            'site_type',
        )

    def create(self, validated_data):
        sampling_event_type = self.context['sampling_event_type']
        validated_data['sampling_event_type'] = sampling_event_type
        return super().create(validated_data)
