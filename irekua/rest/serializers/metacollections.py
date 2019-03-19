# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db
from .users import SelectSerializer as UserSerializer
from .items import SelectSerializer as ItemSerializer


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.MetaCollection
        fields = (
            'url',
            'name',
            'description',
        )


class DetailSerializer(serializers.ModelSerializer):
    creator = UserSerializer(
        many=False,
        read_only=True)
    items = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='api-rest:item-detail')

    class Meta:
        model = db.MetaCollection
        fields = (
            'url',
            'name',
            'description',
            'creator',
            'items',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.MetaCollection
        fields = (
            'name',
            'description',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        return db.MetaCollection.objects.create(
            creator=user,
            **validated_data)
