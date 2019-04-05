# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import CollectionType
from database.models import ItemType
from database.models import EventType
from database.models import DeviceType
from database.models import Role
from database.models import User

from rest.serializers.object_types.data_collections import collection_types
from rest.serializers.object_types.data_collections import collection_sampling_event_types
from rest.serializers.object_types.data_collections import collection_licence_types
from rest.serializers.object_types.data_collections import collection_annotation_types
from rest.serializers.object_types.data_collections import collection_site_types
from rest.serializers.object_types.data_collections import collection_administrators
from rest.serializers.object_types.data_collections import collection_event_types
from rest.serializers.object_types.data_collections import collection_item_types
from rest.serializers.object_types import device_types
from rest.serializers.users import roles
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.filters import CollectionTypeFilter

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.views.utils import AdditionalActionsMixin


class CollectionTypeViewSet(SerializerMappingMixin,
                            AdditionalActionsMixin,
                            PermissionMappingMixin,
                            ModelViewSet):
    queryset = CollectionType.objects.all()
    filterset_class = CollectionTypeFilter

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
    serializer_mapping = (
        SerializerMapping
        .from_module(collection_types)
        .extend(
            administrators=collection_administrators.ListSerializer,
            add_administrator=collection_administrators.CreateSerializer,

            site_types=collection_site_types.ListSerializer,
            add_site_type=collection_site_types.CreateSerializer,

            annotation_types=collection_annotation_types.ListSerializer,
            add_annotation_type=collection_annotation_types.CreateSerializer,

            licence_types=collection_licence_types.ListSerializer,
            add_licence_type=collection_licence_types.CreateSerializer,

            sampling_event_types=collection_sampling_event_types.ListSerializer,
            add_sampling_event_type=collection_sampling_event_types.CreateSerializer,

            item_types=collection_item_types.ListSerializer,
            add_item_type=collection_item_types.CreateSerializer,

            event_types=collection_event_types.ListSerializer,
            add_event_type=collection_event_types.CreateSerializer,

            add_device_type=collection_types.DeviceTypeSerializer,
            remove_device_type=device_types.SelectSerializer,

            add_role=collection_types.RoleSerializer,
            remove_role=roles.SelectSerializer,
        ))

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            collection_type = self.get_object()
        except (AttributeError, AssertionError):
            collection_type = None

        context['collection_type'] = collection_type
        return context

    @action(detail=True, methods=['GET'])
    def site_types(self, request, pk=None):
        model = CollectionType.site_types.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @site_types.mapping.post
    def add_site_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def administrators(self, request, pk=None):
        model = CollectionType.administrators.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @administrators.mapping.post
    def add_administrator(self, request, pk=None):
        return self.add_related_object_view(
            User,
            'administrator',
            pk_field='username')

    @action(detail=True, methods=['GET'])
    def annotation_types(self, request, pk=None):
        model = CollectionType.annotation_types.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @annotation_types.mapping.post
    def add_annotation_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def licence_types(self, request, pk=None):
        model = CollectionType.licence_types.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @licence_types.mapping.post
    def add_licence_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sampling_event_types(self, request, pk=None):
        model = CollectionType.sampling_event_types.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @sampling_event_types.mapping.post
    def add_sampling_event_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def item_types(self, request, pk=None):
        collection_type = self.get_object()
        queryset = collection_type.collectionitemtype_set.all()
        return self.list_related_object_view(queryset)

    @item_types.mapping.post
    def add_item_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def event_types(self, request, pk=None):
        model = CollectionType.event_types.through
        collection_id = self.kwargs['pk']
        queryset = model.objects.filter(collectiontype_id=collection_id)
        return self.list_related_object_view(queryset)

    @event_types.mapping.post
    def add_event_type(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['POST'])
    def add_device_type(self, request, pk=None):
        return self.add_related_object_view(
            DeviceType,
            'device_type',
            extra=['metadata_schema'])

    @action(detail=True, methods=['POST'])
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(detail=True, methods=['POST'])
    def add_role(self, request, pk=None):
        return self.add_related_object_view(
            Role,
            'role',
            extra=['metadata_schema'])

    @action(detail=True, methods=['POST'])
    def remove_role(self, request, pk=None):
        return self.remove_related_object_view(
            'role')
