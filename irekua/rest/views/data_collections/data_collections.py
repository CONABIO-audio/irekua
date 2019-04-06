# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import Collection
from database.models import CollectionType

from rest.serializers import items as item_serializers
from rest.serializers import licences as licence_serializers
from rest.serializers.object_types.data_collections import collection_types
from rest.serializers.sampling_events import sampling_events as sampling_event_serializers
from rest.serializers.data_collections import data_collections
from rest.serializers.data_collections import collection_devices
from rest.serializers.data_collections import collection_sites
from rest.serializers.data_collections import collection_users
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.utils import Actions

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import data_collections as permissions

from rest.filters import CollectionFilter
from rest.views.utils import AdditionalActionsMixin


class CollectionViewSet(SerializerMappingMixin,
                        AdditionalActionsMixin,
                        PermissionMappingMixin,
                        ModelViewSet):
    queryset = Collection.objects.all()
    search_fields = ('name', )
    filterset_class = CollectionFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(data_collections)
        .extend(
            licences=licence_serializers.ListSerializer,
            add_licence=licence_serializers.CreateSerializer,
            devices=collection_devices.ListSerializer,
            add_device=collection_devices.CreateSerializer,
            sites=collection_sites.ListSerializer,
            add_site=collection_sites.CreateSerializer,
            users=collection_users.ListSerializer,
            add_user=collection_users.CreateSerializer,
            sampling_events=sampling_event_serializers.ListSerializer,
            add_sampling_event=sampling_event_serializers.CreateSerializer,
            types=collection_types.ListSerializer,
            add_type=collection_types.CreateSerializer,
            items=item_serializers.ListSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.HasUpdatePermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsCollectionAdmin | IsAdmin
        ],
        'licences': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                IsSpecialUser
            ),
        ],
        'add_licence': [
            IsAuthenticated,
            (
                permissions.HasAddLicencePermission |
                permissions.IsCollectionAdmin
            ),
        ],
        'devices': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        'add_device': [
            IsAuthenticated,
            (
                permissions.HasAddDevicePermission |
                permissions.IsCollectionAdmin |
                IsAdmin
            )
        ],
        'sites': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        'add_site': [
            IsAuthenticated,
            (
                permissions.HasAddSitePermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
        'users': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        'add_user': [
            IsAuthenticated,
            (
                permissions.HasAddUserPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
        'sampling_events': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        'add_sampling_event': [
            IsAuthenticated,
            (
                permissions.HasAddItemPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
        'items': [
            IsAuthenticated,
            (
                permissions.IsCollectionUser |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        'add_type': [IsAuthenticated, IsAdmin]
    }, default=IsAuthenticated)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            collection = self.get_object()
        except (KeyError, AssertionError, AttributeError):
            collection = None
        context['collection'] = collection
        return context

    @action(detail=True, methods=['GET'])
    def licences(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.licence_set.all()
        return self.list_related_object_view(queryset)

    @licences.mapping.post
    def add_licence(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def devices(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectiondevice_set.all()
        return self.list_related_object_view(queryset)

    @devices.mapping.post
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sites(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionsite_set.all()
        return self.list_related_object_view(queryset)

    @sites.mapping.post
    def add_site(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def users(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionuser_set.all()
        return self.list_related_object_view(queryset)

    @users.mapping.post
    def add_user(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sampling_events(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.samplingevent_set.all()
        return self.list_related_object_view(queryset)

    @sampling_events.mapping.post
    def add_sampling_event(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = CollectionType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        collection = self.get_object()
        queryset = db.Item.objects.filter(
            sampling_event_device__sampling_event__collection=collection)
        return self.list_related_object_view(queryset)
