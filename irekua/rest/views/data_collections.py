# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db

from rest.serializers import data_collections
from rest.serializers import licences
from rest.serializers import items as item_serializers
from rest.serializers import sampling_events as sampling_event_serializers
from rest.serializers import collection_devices
from rest.serializers import collection_sites
from rest.serializers import collection_users

from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.Collection
        fields = (
            'name',
            'collection_type__name',
            'institution__institution_code',
            'institution__institution_name',
            'institution__country',
        )


class CollectionViewSet(BaseViewSet, AdditionalActions):
    queryset = db.Collection.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
    serializer_module = data_collections

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            collection = self.get_object()
        except (KeyError, AssertionError):
            collection = None
        context['collection'] = collection
        return context

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=licences.CreateSerializer)
    def create_licence(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=collection_devices.ListSerializer)
    def devices(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectiondevice_set.all()
        return self.list_related_object_view(queryset)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_devices.CreateSerializer)
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=collection_sites.ListSerializer)
    def sites(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionsite_set.all()
        return self.list_related_object_view(queryset)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_sites.CreateSerializer)
    def add_site(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=collection_users.ListSerializer)
    def users(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.collectionuser_set.all()
        return self.list_related_object_view(queryset)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=collection_users.CreateSerializer)
    def add_user(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=sampling_event_serializers.ListSerializer)
    def sampling_events(self, request, pk=None):
        collection = self.get_object()
        queryset = collection.samplingevent_set.all()
        return self.list_related_object_view(queryset)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_serializers.CreateSerializer)
    def add_sampling_event(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=item_serializers.ListSerializer)
    def items(self, request, pk=None):
        collection = self.get_object()
        queryset = db.Item.objects.filter(
            sampling_event__collection=collection)
        return self.list_related_object_view(queryset)
