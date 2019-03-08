# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename')


    class Meta:
        model = db.Role
        fields = (
            'url',
            'name',
            'description',
            'permissions',
            'icon',
        )
