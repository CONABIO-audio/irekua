# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Collection
        fields = (
            'url',
            'name',
            'description',
            'metadata_type',
            'metadata',
            'coordinator',
            'institution',
            'is_open'
        )
