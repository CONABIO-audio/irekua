# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

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
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.filters import CollectionTypeFilter

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from .utils import AdditionalActionsMixin



class CollectionTypeViewSet(SerializerMappingMixin,
                            AdditionalActionsMixin,
                            PermissionMappingMixin,
                            ModelViewSet):
    queryset = db.CollectionType.objects.all()
    filterset_class = CollectionTypeFilter

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
    serializer_mapping = (
        SerializerMapping
        .from_module(collection_types)
        .extend(
            add_annotation_type=annotation_types.SelectSerializer,
            remove_annotation_type=annotation_types.SelectSerializer,
            add_licence_type=licence_types.SelectSerializer,
            remove_licence_type=licence_types.SelectSerializer,
            add_sampling_event_type=sampling_event_types.SelectSerializer,
            remove_sampling_event_type=sampling_event_types.SelectSerializer,
            add_site_type=site_types.SelectSerializer,
            remove_site_type=site_types.SelectSerializer,
            add_item_type=collection_types.ItemTypeSerializer,
            remove_item_type=item_types.SelectSerializer,
            add_event_type=event_types.SelectSerializer,
            remove_event_type=event_types.SelectSerializer,
            add_device_type=collection_types.DeviceTypeSerializer,
            remove_device_type=device_types.SelectSerializer,
            add_role=collection_types.RoleSerializer,
            remove_role=roles.SelectSerializer,
            add_administrator=collection_types.UserSerializer,
            remove_administrator=collection_types.UserSerializer
        ))

    @action(detail=True, methods=['POST'])
    def add_annotation_type(self, request, pk=None):
        return self.add_related_object_view(
            db.AnnotationType,
            'annotation_type')

    @action(detail=True, methods=['POST'])
    def remove_annotation_type(self, request, pk=None):
        return self.remove_related_object_view(
            'annotation_type')

    @action(detail=True, methods=['POST'])
    def add_licence_type(self, request, pk=None):
        return self.add_related_object_view(
            db.LicenceType,
            'licence_type')

    @action(detail=True, methods=['POST'])
    def remove_licence_type(self, request, pk=None):
        return self.remove_related_object_view(
            'licence_type')

    @action(detail=True, methods=['POST'])
    def add_sampling_event_type(self, request, pk=None):
        return self.add_related_object_view(
            db.SamplingEventType,
            'sampling_event_type')

    @action(detail=True, methods=['POST'])
    def remove_sampling_event_type(self, request, pk=None):
        return self.remove_related_object_view(
            'sampling_event_type')

    @action(detail=True, methods=['POST'])
    def add_site_type(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(detail=True, methods=['POST'])
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')

    @action(detail=True, methods=['POST'])
    def add_item_type(self, request, pk=None):
        return self.add_related_object_view(
            db.ItemType,
            'item_type',
            extra=['metadata_schema'])

    @action(detail=True, methods=['POST'])
    def remove_item_type(self, request, pk=None):
        return self.remove_related_object_view(
            'item_type')

    @action(detail=True, methods=['POST'])
    def add_event_type(self, request, pk=None):
        return self.add_related_object_view(
            db.EventType,
            'event_type')

    @action(detail=True, methods=['POST'])
    def remove_event_type(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')

    @action(detail=True, methods=['POST'])
    def add_device_type(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type',
            extra=['metadata_schema'])

    @action(detail=True, methods=['POST'])
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(detail=True, methods=['POST'])
    def add_role(self, request, pk=None):
        return self.add_related_object_view(
            db.Role,
            'role',
            extra=['metadata_schema'])

    @action(detail=True, methods=['POST'])
    def remove_role(self, request, pk=None):
        return self.remove_related_object_view(
            'role')

    @action(detail=True, methods=['POST'])
    def add_administrator(self, request, pk=None):
        return self.add_related_object_view(
            db.User,
            'administrator',
            pk_field='username')

    @action(detail=True, methods=['POST'])
    def remove_administrator(self, request, pk=None):
        return self.remove_related_object_view(
            'administrator',
            pk_field='username')
