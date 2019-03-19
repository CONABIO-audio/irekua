# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db
from rest.serializers import collection_types
from rest.serializers import event_types
from rest.serializers import item_types
from rest.serializers import annotation_types
from rest.serializers import licence_types
from rest.serializers import sampling_event_types
from rest.serializers import device_types
from rest.serializers import site_types
from rest.serializers import roles

from rest.filters import BaseFilter
from .utils import AdditionalActions, BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.CollectionType
        fields = (
            'name',
            'anyone_can_create',
        )


class CollectionTypeViewSet(BaseViewSet, AdditionalActions):
    queryset = db.CollectionType.objects.all()
    serializer_module = collection_types
    filterset_class = Filter

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=annotation_types.SelectSerializer)
    def add_annotation_type(self, request, pk=None):
        return self.add_related_object_view(
            db.AnnotationType,
            'annotation_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=annotation_types.SelectSerializer)
    def remove_annotation_type(self, request, pk=None):
        return self.remove_related_object_view(
            'annotation_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=licence_types.SelectSerializer)
    def add_licence_type(self, request, pk=None):
        return self.add_related_object_view(
            db.LicenceType,
            'licence_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=licence_types.SelectSerializer)
    def remove_licence_type(self, request, pk=None):
        return self.remove_related_object_view(
            'licence_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.SelectSerializer)
    def add_sampling_event_type(self, request, pk=None):
        return self.add_related_object_view(
            db.SamplingEventType,
            'sampling_event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.SelectSerializer)
    def remove_sampling_event_type(self, request, pk=None):
        return self.remove_related_object_view(
            'sampling_event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=site_types.SelectSerializer)
    def add_site_type(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=site_types.SelectSerializer)
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_types.ItemTypeSerializer)
    def add_item_type(self, request, pk=None):
        return self.add_related_object_view(
            db.ItemType,
            'item_type',
            extra=['metadata_schema'])

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=item_types.SelectSerializer)
    def remove_item_type(self, request, pk=None):
        return self.remove_related_object_view(
            'item_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=event_types.SelectSerializer)
    def add_event_type(self, request, pk=None):
        return self.add_related_object_view(
            db.EventType,
            'event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=event_types.SelectSerializer)
    def remove_event_type(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_types.DeviceTypeSerializer)
    def add_device_type(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type',
            extra=['metadata_schema'])

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=device_types.SelectSerializer)
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_types.RoleSerializer)
    def add_role(self, request, pk=None):
        return self.add_related_object_view(
            db.Role,
            'role',
            extra=['metadata_schema'])

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=roles.SelectSerializer)
    def remove_role(self, request, pk=None):
        return self.remove_related_object_view(
            'role')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_types.UserSerializer)
    def add_administrator(self, request, pk=None):
        return self.add_related_object_view(
            db.User,
            'administrator',
            pk_field='username')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_types.UserSerializer)
    def remove_administrator(self, request, pk=None):
        return self.remove_related_object_view(
            'administrator',
            pk_field='username')
