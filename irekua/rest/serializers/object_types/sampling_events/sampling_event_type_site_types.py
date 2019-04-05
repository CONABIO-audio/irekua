# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import SamplingEventType
from database.models import SiteType

from rest.serializers.object_types import site_types
from . import sampling_event_types


MODEL = SamplingEventType.site_types.through


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=True,
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'site_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    site_type = site_types.SelectSerializer(
        many=False,
        read_only=True,
        source='sitetype')
    sampling_event_type = sampling_event_types.SelectSerializer(
        many=False,
        read_only=True,
        source='samplingeventtype')

    class Meta:
        model = MODEL
        fields = (
            'url',
            'id',
            'sampling_event_type',
            'site_type',
        )


class CreateSerializer(serializers.ModelSerializer):
    site_type = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=SiteType.objects.all(),
        source='sitetype')

    class Meta:
        model = MODEL
        fields = (
            'site_type',
        )

    def create(self, validated_data):
        sampling_event_type = self.context['sampling_event_type']
        validated_data['samplingeventtype'] = sampling_event_type
        return super().create(validated_data)
