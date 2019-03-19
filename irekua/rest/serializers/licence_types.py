# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class SelectSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.LicenceType.objects.all())

    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
            'description',
            'icon',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'name',
            'description',
            'metadata_schema',
            'document_template',
            'years_valid_for',
            'icon',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations',
        )
