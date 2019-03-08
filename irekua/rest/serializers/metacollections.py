# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class MetaCollectionSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='user-detail')
    items = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='item-detail')

    class Meta:
        model = db.MetaCollection
        fields = (
            'url',
            'name',
            'description',
            'creator',
            'items',
        )
