# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database import models
from rest import filters
from rest import utils
from rest import serializers

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsSpecialUser
from rest.permissions import data_collections as permissions


class CollectionViewSet(utils.CustomViewSetMixin, ModelViewSet):
    queryset = models.Collection.objects.all()  # pylint: disable=E1101
    search_fields = filters.data_collections.search_fields
    filterset_class = filters.data_collections.Filter

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.data_collections.data_collections)
        .extend(
            metacollections=serializers.data_collections.metacollections.ListSerializer,
            add_metacollection=serializers.data_collections.metacollections.CreateSerializer,
            licences=serializers.licences.ListSerializer,
            add_licence=serializers.licences.CreateSerializer,
            devices=serializers.data_collections.devices.ListSerializer,
            add_device=serializers.data_collections.devices.CreateSerializer,
            sites=serializers.data_collections.sites.ListSerializer,
            add_site=serializers.data_collections.sites.CreateSerializer,
            users=serializers.data_collections.users.ListSerializer,
            add_user=serializers.data_collections.users.CreateSerializer,
            sampling_events=serializers.sampling_events.sampling_events.ListSerializer,
            add_sampling_event=serializers.sampling_events.sampling_events.CreateSerializer,
            types=serializers.object_types.data_collections.types.ListSerializer,
            add_type=serializers.object_types.data_collections.types.CreateSerializer,
            licence_types=serializers.object_types.licences.ListSerializer,
            add_licence_type=serializers.object_types.licences.CreateSerializer,
            items=serializers.items.items.ListSerializer,
            administrators=serializers.data_collections.administrators.ListSerializer,
            add_administrator=serializers.data_collections.administrators.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.HasUpdatePermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
        utils.Actions.DESTROY: [
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
        'add_type': [IsAuthenticated, IsAdmin],
        'add_administrator': [
            IsAuthenticated,
            (
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
    })

    def get_object(self):
        collection_id = self.kwargs['pk']
        collection = get_object_or_404(models.Collection, pk=collection_id)

        self.check_object_permissions(self.request, collection)
        return collection

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
            return models.MetaCollection.objects.all()  # pylint: disable=E1101

        if self.action == 'licences':
            collection_id = self.kwargs['pk']
            return models.Licence.objects.filter(collection=collection_id)  # pylint: disable=E1101

        if self.action == 'devices':
            collection_id = self.kwargs['pk']
            return models.CollectionDevice.objects.filter(collection=collection_id)  # pylint: disable=E1101

        if self.action == 'sites':
            collection_id = self.kwargs['pk']
            return models.CollectionSite.objects.filter(collection=collection_id)  # pylint: disable=E1101

        if self.action == 'users':
            collection_id = self.kwargs['pk']
            return models.CollectionUser.objects.filter(collection=collection_id)  # pylint: disable=E1101

        if self.action == 'sampling_events':
            collection_id = self.kwargs['pk']
            return models.SamplingEvent.objects.filter(collection=collection_id)  # pylint: disable=E1101

        if self.action == 'types':
            return models.CollectionType.objects.all()  # pylint: disable=E1101

        if self.action == 'licence_types':
            return models.LicenceType.objects.all()  # pylint: disable=E1101

        if self.action == 'items':
            collection_id = self.kwargs['pk']
            return models.Item.objects.filter(  # pylint: disable=E1101
                sampling_event_device__sampling_event__collection=collection_id)

        if self.action == 'administrators':
            model = models.Collection.administrators.through
            collection_id = self.kwargs['pk']
            return model.objects.filter(collection=collection_id)

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
        filterset_class=filters.collection_administrators.Filter,
        search_fields=filters.collection_administrators.search_fields)
    def administrators(self, request, pk=None):
        return self.list_related_object_view()

    @administrators.mapping.post
    def add_administrator(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()
