# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import data_collections
from rest.serializers import licences
from rest.serializers import items as item_serializers
from rest.serializers import sampling_events as sampling_event_serializers
from rest.serializers import collection_devices
from rest.serializers import collection_sites
from rest.serializers import collection_users
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import CollectionFilter
from .utils import AdditionalActionsMixin


class CollectionViewSet(SerializerMappingMixin,
                        AdditionalActionsMixin,
                        ModelViewSet):
    queryset = db.Collection.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = CollectionFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(data_collections)
        .extend(
            create_licence=licences.CreateSerializer,
            devices=collection_devices.ListSerializer,
            add_device=collection_devices.CreateSerializer,
            sites=collection_sites.ListSerializer,
            add_site=collection_sites.CreateSerializer,
            users=collection_users.ListSerializer,
            add_user=collection_users.CreateSerializer,
            sampling_events=sampling_event_serializers.ListSerializer,
            add_sampling_event=sampling_event_serializers.CreateSerializer,
            items=item_serializers.ListSerializer
        ))

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            collection = self.get_object()
        except (KeyError, AssertionError):
            collection = None
        context['collection'] = collection
        return context

    @action(detail=True, methods=['POST'])
    def create_licence(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def devices(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectiondevice_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sites(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionsite_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def add_site(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def users(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionuser_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def add_user(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def sampling_events(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.samplingevent_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def add_sampling_event(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        collection = self.get_object()
        queryset = db.Item.objects.filter(
            sampling_event__collection=collection)
        return self.list_related_object_view(queryset)
