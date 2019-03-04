# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class MetaCollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.MetaCollection
        fields = (
            'url',
            'name',
            'description',
            'creator',
            'items',
        )
