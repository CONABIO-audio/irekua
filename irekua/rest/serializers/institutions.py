# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Institution.objects.all())

    class Meta:
        model = db.Institution
        fields = (
            'url',
            'id',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Institution
        fields = (
            'url',
            'institution_code',
            'subdependency',
            'logo',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Institution
        fields = (
            'url',
            'id',
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country',
            'postal_code',
            'address',
            'website',
            'logo',
        )
