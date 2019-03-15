# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class MetaCollectionSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')
    creator_url = serializers.HyperlinkedRelatedField(
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
            'creator_url',
            'items',
        )

    def create(self, validated_data):
        user = self.context['request'].user
        return db.MetaCollection.objects.create(
            creator=user,
            **validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data['description']
        instance.save()
        return instance
