# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.DeviceBrand.objects.all())

    class Meta:
        model = db.DeviceBrand
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'url',
            'name',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'url',
            'name',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.DeviceBrand
        fields = (
            'name',
            'website',
            'logo',
        )
