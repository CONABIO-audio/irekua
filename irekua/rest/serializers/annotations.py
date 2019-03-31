# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    annotation = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Annotation.objects.all())

    class Meta:
        model = db.Annotation
        fields = (
            'url',
            'annotation',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Annotation
        fields = (
            'url',
            'item',
            'event_type',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Annotation
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
    class Meta:
        model = db.Annotation
        fields = (
            'event_type',
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
        user = self.context['user']

        validated_data['item'] = item
        validated_data['created_by'] = user
        validated_data['modified_by'] = user

        super().create(validated_data)

    def update(self, validated_data):
        user = self.context['user']

        validated_data['modified_by'] = user
        super().update(validated_data)
