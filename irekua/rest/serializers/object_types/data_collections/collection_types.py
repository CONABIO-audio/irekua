# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers

from database.models import CollectionType
from database.models import ItemType
from database.models import CollectionItemType
from database.models import Role
from database.models import CollectionRole
from database.models import DeviceType
from database.models import CollectionDeviceType



class SelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
        )


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'logo',
            'description',
        )


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'name',
            'logo',
            'description',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionType
        fields = (
            'logo',
            'description',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
        )

class DeviceTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:devicetype-detail',
        source='device_type')
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=DeviceType.objects.all(),
        source='device_type')

    class Meta:
        model = CollectionDeviceType
        fields = (
            'url',
            'name',
            'metadata_schema',
        )


class ItemTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:itemtype-detail',
        source='item_type')
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=ItemType.objects.all(),
        source='item_type')

    class Meta:
        model = CollectionItemType
        fields = (
            'url',
            'name',
            'metadata_schema',
        )


class RoleSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:role-detail',
        source='role')
    name = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=Role.objects.all(),
        source='role',
        slug_field='name')

    class Meta:
        model = CollectionRole
        fields = (
            'url',
            'name',
            'metadata_schema',
        )


class DetailSerializer(serializers.HyperlinkedModelSerializer):
    device_types = DeviceTypeSerializer(
        many=True,
        read_only=True,
        source='collectiondevicetype_set')
    item_types = ItemTypeSerializer(
        many=True,
        read_only=True,
        source='collectionitemtype_set')
    roles = RoleSerializer(
        many=True,
        read_only=True,
        source='collectionrole_set')

    class Meta:
        model = CollectionType
        fields = (
            'url',
            'name',
            'description',
            'logo',
            'metadata_schema',
            'anyone_can_create',
            'restrict_site_types',
            'restrict_annotation_types',
            'restrict_item_types',
            'restrict_licence_types',
            'restrict_device_types',
            'restrict_event_types',
            'restrict_sampling_event_types',
            'item_types',
            'device_types',
            'roles',
            'created_on',
            'modified_on',
        )
