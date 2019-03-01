# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionUser
        fields = (
            'url',
            'collection',
            'user',
            'role',
            'metadata_type',
            'metadata',
            'is_admin',
        )
