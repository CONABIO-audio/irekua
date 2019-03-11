# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionRoleSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection_type-detail')
    role = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='role-detail')

    class Meta:
        model = db.CollectionRole
        fields = (
            'url',
            'collection_type',
            'role',
            'metadata_schema'
        )
