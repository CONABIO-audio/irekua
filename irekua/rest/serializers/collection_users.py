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
    role = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name')

    class Meta:
        model = db.CollectionUser
        fields = (
            'url',
            'user',
            'role',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    user = users.DetailSerializer(many=False, read_only=True)
    role = roles.DetailSerializer(many=False, read_only=True)

    class Meta:
        model = db.CollectionUser
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
        model = db.CollectionUser
        fields = (
            'user',
            'role',
            'metadata',
        )

    def create(self, validated_data):
        collection = self.context['collection']
        validated_data['collection'] = collection
        return super().create(validated_data)
