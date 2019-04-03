# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
            'description',
            'icon'
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
            'description',
            'annotation_schema',
            'icon',
            'created_on',
            'modified_on'
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'name',
            'description',
            'annotation_schema',
            'icon',
        )
