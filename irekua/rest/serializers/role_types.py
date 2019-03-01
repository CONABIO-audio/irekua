# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class RoleTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.RoleType
        fields = (
            'url',
            'description',
            'permissions',
        )
