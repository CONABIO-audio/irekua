# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
import database.models as db


class ListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionType
        fields = (
            'url',
            'name',
            'logo',
            'description',
        )


class CreateAndUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.CollectionType
        fields = (
            'url',
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


class SiteTypeSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.SiteType.objects.all())

    class Meta:
        model = db.SiteType
        fields = (
            'url',
            'name')


class AnnotationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.AnnotationType
        fields = (
            'url',
            'name',
        )


class ItemTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:itemtype-detail',
        source='item_type')
    item_type = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        queryset=db.ItemType.objects.all(),
        slug_field='name')

    class Meta:
        model = db.CollectionItemType
        fields = (
            'url',
            'item_type',
            'metadata_schema',
        )


class TermTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.TermType
        fields = (
            'url',
            'name'
        )


class EventTypeSerializer(serializers.ModelSerializer):
    name = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.EventType.objects.all())

    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name',
        )


class LicenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.LicenceType
        fields = (
            'url',
            'name',
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
        queryset=db.DeviceType.objects.all(),
        source='device_type')

    class Meta:
        model = db.CollectionDeviceType
        fields = (
            'url',
            'name',
            'metadata_schema',
        )


class SamplingEventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.SamplingEventType
        fields = (
            'url',
            'name',
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
        queryset=db.Role.objects.all(),
        source='role',
        slug_field='name')

    class Meta:
        model = db.CollectionRole
        fields = (
            'url',
            'name',
            'metadata_schema'
        )


class UserSerializer(serializers.ModelSerializer):
    username = serializers.PrimaryKeyRelatedField(
        many=False,
        read_only=False,
        queryset=db.User.objects.all())

    class Meta:
        model = db.User
        fields = (
            'url',
            'username',
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
        read_only=True)
    administrators = UserSerializer(
        many=True,
        read_only=False)

    class Meta:
        model = db.CollectionType
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
        )
