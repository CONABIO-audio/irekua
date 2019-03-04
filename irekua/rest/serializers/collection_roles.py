# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class CollectionRoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionRoleType
        fields = (
            'url',
            'collection',
            'role_type'
        )
