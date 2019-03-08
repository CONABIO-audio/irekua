# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionUserSerializer(serializers.HyperlinkedModelSerializer):
    collection = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='collection-detail')
    user = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')
    role = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='role-detail')

    class Meta:
        model = db.CollectionUser
        fields = (
            'url',
            'collection',
            'user',
            'role',
            'metadata',
            'is_admin',
        )
