# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

import database.models as db
from . import collection_types
from . import institutions
from . import licences


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Collection
        fields = (
            'url',
            'name',
            'logo',
            'collection_type',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = collection_types.ListSerializer(
        many=False,
        read_only=False)
    institution = institutions.ListSerializer(
        many=False,
        read_only=True)
    licence_set = licences.ListSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = db.Collection
        fields = (
            'url',
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
            'licence_set',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
        )
