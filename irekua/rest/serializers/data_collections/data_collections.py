# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import Collection
from database.models import CollectionUser

from rest.serializers.object_types.data_collections import collection_types
from rest.serializers.users import institutions
from rest.serializers import licences
from rest.serializers.data_collections import collection_users


class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
            'logo',
            'collection_type',
            'description',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    collection_type = collection_types.SelectSerializer(
        many=False,
        read_only=False)
    institution = institutions.SelectSerializer(
        many=False,
        read_only=True)
    licence_set = licences.SelectSerializer(
        many=True,
        read_only=True)

    class Meta:
        model = Collection
        fields = (
            'url',
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'logo',
            'licence_set',
            'created_on',
            'modified_on',
        )


class CreateSerializer(serializers.ModelSerializer):
    user_data = collection_users.CreateSerializer(
        many=False,
        read_only=False)

    class Meta:
        model = Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
            'user_data',
        )

    def create(self, validated_data):
        user = self.context['request'].user

        user_data = validated_data.pop('user_data')
        collection = Collection.objects.create(**validated_data)

        user_data['user'] = user
        user_data['collection'] = collection
        user_data['is_admin'] = True
        CollectionUser.objects.create(**user_data)

        # Strange loading condition requires this line to be called
        # in order to correctly return parsed data in HTTP response
        self.data

        return collection


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = (
            'name',
            'collection_type',
            'description',
            'logo',
            'metadata',
            'institution',
        )
