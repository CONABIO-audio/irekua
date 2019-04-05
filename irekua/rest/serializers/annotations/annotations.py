# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Annotation


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'item',
            'event_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Annotation
        fields = (
            'url',
            'id',
            'annotation_tool',
            'item',
            'event_type',
            'label',
            'annotation_type',
            'annotation',
            'annotation_configuration',
            'certainty',
            'quality',
            'commentaries',
            'created_on',
            'modified_on',
            'created_by',
            'modified_by',
        )


class CreateSerializer(serializers.ModelSerializer):
    label = serializers.JSONField()

    class Meta:
        model = Annotation
        fields = (
            'event_type',
            'annotation',
            'label',
            'certainty',
            'quality',
            'commentaries',
            'annotation_tool',
            'annotation_configuration',
            'annotation_type',
        )

    def create(self, validated_data):
        item = self.context['item']
        user = self.context['request'].user

        validated_data['item'] = item
        validated_data['created_by'] = user
        validated_data['modified_by'] = user

        return super().create(validated_data)

    def update(self, validated_data):
        user = self.context['request'].user

        validated_data['modified_by'] = user
        return super().update(validated_data)
