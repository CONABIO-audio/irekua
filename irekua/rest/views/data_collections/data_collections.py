# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import Collection
from database.models import SamplingEvent
from database.models import MetaCollection
from database.models import CollectionType
from database.models import CollectionDevice
from database.models import CollectionSite
from database.models import CollectionUser
from database.models import LicenceType
from database.models import Licence
from database.models import Item

from rest.serializers.items import items as item_serializers
from rest.serializers import licences as licence_serializers
from rest.serializers.object_types.data_collections import collection_types
from rest.serializers.object_types import licence_types as licence_type_serializers
from rest.serializers.sampling_events import sampling_events as sampling_event_serializers
from rest.serializers.data_collections import data_collections
from rest.serializers.data_collections import collection_devices
from rest.serializers.data_collections import collection_sites
from rest.serializers.data_collections import collection_users
from rest.serializers.data_collections import metacollections as metacollection_serializers

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsSpecialUser
from rest.permissions import data_collections as permissions

from rest import filters

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class CollectionViewSet(CustomViewSetMixin, ModelViewSet):
    queryset = Collection.objects.all()
    search_fields = filters.data_collections.search_fields
    filterset_class = filters.data_collections.Filter

    serializer_mapping = (
        SerializerMapping
        .from_module(data_collections)
        .extend(
            metacollections=metacollection_serializers.ListSerializer,
            add_metacollection=metacollection_serializers.CreateSerializer,
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
            licence_types=licence_type_serializers.ListSerializer,
            add_licence_type=licence_type_serializers.CreateSerializer,
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
        'add_licence_type': [
            IsAuthenticated, IsAdmin
        ],
        'add_metacollection': [
            IsAuthenticated, IsAdmin | IsDeveloper
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

    def get_queryset(self):
        if self.action == 'metacollections':
            return MetaCollection.objects.all()

        if self.action == 'licences':
            collection_id = self.kwargs['pk']
            return Licence.objects.filter(collection=collection_id)

        if self.action == 'devices':
            collection_id = self.kwargs['pk']
            return CollectionDevice.objects.filter(collection=collection_id)

        if self.action == 'sites':
            collection_id = self.kwargs['pk']
            return CollectionSite.objects.filter(collection=collection_id)

        if self.action == 'users':
            collection_id = self.kwargs['pk']
            return CollectionUser.objects.filter(collection=collection_id)

        if self.action == 'sampling_events':
            collection_id = self.kwargs['pk']
            return SamplingEvent.objects.filter(collection=collection_id)

        if self.action == 'types':
            return CollectionType.objects.all()

        if self.action == 'licence_types':
            return LicenceType.objects.all()

        if self.action == 'items':
            collection_id = self.kwargs['pk']
            return Item.objects.filter(
                sampling_event_device__sampling_event__collection=collection_id)

        return super().get_queryset()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.metacollections.Filter,
        search_fields=filters.metacollections.search_fields)
    def metacollections(self, request):
        return self.list_related_object_view()

    @metacollections.mapping.post
    def add_metacollection(self, request):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.licences.Filter,
        search_fields=filters.licences.search_fields)
    def licences(self, request, pk=None):
        return self.list_related_object_view()

    @licences.mapping.post
    def add_licence(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.collection_devices.Filter,
        search_fields=filters.collection_devices.search_fields)
    def devices(self, request, pk=None):
        return self.list_related_object_view()

    @devices.mapping.post
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.collection_sites.Filter,
        search_fields=filters.collection_sites.search_fields)
    def sites(self, request, pk=None):
        return self.list_related_object_view()

    @sites.mapping.post
    def add_site(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.collection_users.Filter,
        search_fields=filters.collection_users.search_fields)
    def users(self, request, pk=None):
        return self.list_related_object_view()

    @users.mapping.post
    def add_user(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.sampling_events.Filter,
        search_fields=filters.sampling_events.search_fields)
    def sampling_events(self, request, pk=None):
        return self.list_related_object_view()

    @sampling_events.mapping.post
    def add_sampling_event(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.collection_types.Filter,
        search_fields=filters.collection_types.search_fields)
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.licence_types.Filter,
        search_fields=filters.licence_types.search_fields)
    def licence_types(self, request):
        return self.list_related_object_view()

    @licence_types.mapping.post
    def add_licence_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()
