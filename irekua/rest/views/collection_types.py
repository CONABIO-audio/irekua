# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action

import database.models as db
from rest import serializers
from rest.serializers.collection_types import (
    ListSerializer,
    DetailSerializer,
    CreateAndUpdateSerializer,
    SiteTypeSerializer,
    AnnotationTypeSerializer,
    ItemTypeSerializer,
    EventTypeSerializer,
    LicenceTypeSerializer,
    DeviceTypeSerializer,
    SamplingEventTypeSerializer,
    RoleSerializer,
    UserSerializer,
)
from .utils import AdditionalActions


class CollectionTypeViewSet(viewsets.ModelViewSet, AdditionalActions):
    queryset = db.CollectionType.objects.all()
    serializer_class = CreateAndUpdateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ListSerializer
        if self.action == 'retrieve':
            return DetailSerializer
        return super(CollectionTypeViewSet, self).get_serializer_class()

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=AnnotationTypeSerializer)
    def add_annotation_types(self, request, pk=None):
        return self.add_related_object_view(
            db.AnnotationType,
            'annotation_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=AnnotationTypeSerializer)
    def remove_annotation_types(self, request, pk=None):
        return self.remove_related_object_view(
            'annotation_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.AnnotationTypeSerializer)
    def create_annotation_type(self, request, pk=None):
        return self.create_related_object_view(
            db.AnnotationType,
            'annotation_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=EventTypeSerializer)
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(
            db.EventType,
            'event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=LicenceTypeSerializer)
    def remove_licence_types(self, request, pk=None):
        return self.remove_related_object_view(
            'licence_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.LicenceTypeSerializer)
    def create_licence_type(self, request, pk=None):
        return self.create_related_object_view(
            db.LicenceType,
            'licence_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SamplingEventTypeSerializer)
    def add_sampling_event_types(self, request, pk=None):
        return self.add_related_object_view(
            db.SamplingEventType,
            'sampling_event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SamplingEventTypeSerializer)
    def remove_sampling_event_types(self, request, pk=None):
        return self.remove_related_object_view(
            'sampling_event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.SamplingEventTypeSerializer)
    def create_sampling_event_type(self, request, pk=None):
        return self.create_related_object_view(
            db.SamplingEventType,
            'sampling_event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SiteTypeSerializer)
    def add_site_types(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SiteTypeSerializer)
    def remove_site_types(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.SiteTypeSerializer)
    def create_site_type(self, request, pk=None):
        return self.create_related_object_view(
            db.SiteType,
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=ItemTypeSerializer)
    def add_item_types(self, request, pk=None):
        return self.add_related_object_view(
            db.ItemType,
            'item_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=ItemTypeSerializer)
    def remove_item_types(self, request, pk=None):
        return self.remove_related_object_view(
            'item_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.ItemTypeSerializer)
    def create_item_type(self, request, pk=None):
        return self.create_related_object_view(
            db.ItemType,
            'item_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=DeviceTypeSerializer)
    def add_device_types(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=DeviceTypeSerializer)
    def remove_device_types(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=serializers.DeviceTypeSerializer)
    def create_device_type(self, request, pk=None):
        return self.create_related_object_view(
            db.DeviceType,
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=RoleSerializer)
    def add_roles(self, request, pk=None):
        return self.add_related_object_view(
            db.Role,
            'role')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=RoleSerializer)
    def remove_roles(self, request, pk=None):
        return self.remove_related_object_view(
            'role')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=UserSerializer)
    def add_administrators(self, request, pk=None):
        return self.add_related_object_view(
            db.User,
            'administrator',
            pk_field='username')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=UserSerializer)
    def remove_administrators(self, request, pk=None):
        return self.remove_related_object_view(
            'administrator',
            pk_field='username')
