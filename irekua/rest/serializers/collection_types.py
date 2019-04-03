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

from .annotation_types import SelectSerializer as AnnotationTypeSerializer
from .event_types import SelectSerializer as EventTypeSerializer
from .site_types import SelectSerializer as SiteTypeSerializer
from .licence_types import SelectSerializer as LicenceTypeSerializer
from .sampling_event_types import (
        SelectSerializer as SamplingEventTypeSerializer)
from .users import SelectSerializer as UserSerializer



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
    site_types = SiteTypeSerializer(
        many=True,
        read_only=True)
    event_types = EventTypeSerializer(
        many=True,
        read_only=True)
    device_types = DeviceTypeSerializer(
        many=True,
        read_only=True,
        source='collectiondevicetype_set')
    licence_types = LicenceTypeSerializer(
        many=True,
        read_only=True)
    annotation_types = AnnotationTypeSerializer(
        many=True,
        read_only=True)
    sampling_event_types = SamplingEventTypeSerializer(
        many=True,
        read_only=True)
    item_types = ItemTypeSerializer(
        many=True,
        read_only=True,
        source='collectionitemtype_set')
    roles = RoleSerializer(
        many=True,
        read_only=True,
        source='collectionrole_set')
    administrators = UserSerializer(
        many=True,
        read_only=False)

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
            'site_types',
            'annotation_types',
            'item_types',
            'licence_types',
            'device_types',
            'event_types',
            'sampling_event_types',
            'roles',
            'administrators',
            'created_on',
            'modified_on',
        )
