# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection_type-detail')
    devices = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='physical_device-detail')
    sites = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='site-detail')
    users = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')
    licences = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='licence-detail')

    class Meta:
        model = db.Collection
        fields = (
            'url',
            'collection_type',
            'name',
            'description',
            'metadata',
            'institution',
            'logo',
            'devices',
            'sites',
            'users',
            'licences'
        )
