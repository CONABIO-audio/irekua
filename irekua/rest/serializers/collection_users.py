# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from . import users
from . import roles


class SelectSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.CollectionUser.objects.all(),
        source='id')

    class Meta:
        model = db.CollectionUser
        fields = (
            'url',
            'user',
        )


class ListSerializer(serializers.HyperlinkedModelSerializer):
    user = users.ListSerializer(
        many=False,
        read_only=True)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'user',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    user = users.DetailSerializer(many=False, read_only=True)
    role = roles.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = db.CollectionDevice
        fields = (
            'url',
            'user',
            'role',
            'metadata',
            'is_admin',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'user',
            'role',
            'metadata',
        )
