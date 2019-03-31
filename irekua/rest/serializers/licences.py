# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db

from . import licence_types
from . import users


class SelectSerializer(serializers.ModelSerializer):
    licence = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.Licence.objects.all(),
        source='id')

    class Meta:
        model = db.Licence
        fields = (
            'url',
            'licence',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    licence_type = licence_types.ListSerializer(many=False, read_only=True)

    class Meta:
        model = db.Licence
        fields = (
            'url',
            'id',
            'licence_type',
            'created_on',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    licence_type = licence_types.DetailSerializer(many=False, read_only=True)
    signed_by = users.DetailSerializer(many=False, read_only=True)
    collection = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name')

    class Meta:
        model = db.Licence
        fields = (
            'url',
            'id',
            'licence_type',
            'created_on',
            'document',
            'metadata',
            'signed_by',
            'collection',
            'is_active',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Licence
        fields = (
            'licence_type',
            'document',
            'metadata',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.collection = kwargs['context']['collection']
            self.fields['licence_type'].queryset = (
                self.collection.collection_type.licence_types)
        except KeyError:
            pass

    def create(self, validated_data):
        user = self.context['request'].user
        collection = self.context['collection']

        validated_data['signed_by'] = user
        validated_data['collection'] = collection

        return super().create(validated_data)
