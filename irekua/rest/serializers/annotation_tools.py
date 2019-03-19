# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.AnnotationTool.objects.all())

    class Meta:
        model = db.AnnotationTool
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.AnnotationTool
        fields = (
            'url',
            'name',
            'version',
            'description',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.AnnotationTool
        fields = (
            'url',
            'id',
            'name',
            'version',
            'description',
            'logo',
            'website',
            'configuration_schema',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationTool
        fields = (
            'name',
            'version',
            'description',
            'logo',
            'website',
            'configuration_schema',
        )
