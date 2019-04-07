# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database.models import MetaCollection
from database.models import Item

from rest.serializers.data_collections import metacollections
from rest.serializers.items import items as item_serializers

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsSpecialUser
from rest.permissions import IsAuthenticated

from rest import filters

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class MetaCollectionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):
    queryset = MetaCollection.objects.all()
    filterset_class = filters.metacollections.Filter
    search_fields = filters.metacollections.search_fields

    serializer_mapping = (
        SerializerMapping
        .from_module(metacollections)
        .extend(
            items=item_serializers.ListSerializer,
            add_items=item_serializers.SelectSerializer,
            remove_item=item_serializers.SelectSerializer
        ))

    permission_mapping = PermissionMapping({
        Actions.LIST: [
            IsAuthenticated
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            IsSpecialUser
        ],
        'items': [
            IsAuthenticated,
            IsSpecialUser
        ],
    }, default=[
        IsAuthenticated,
        IsDeveloper | IsAdmin
    ])

    def get_queryset(self):
        if self.action == 'items':
            metacollection_id = self.kwargs['pk']
            metacollection = MetaCollection.objects.get(pk=metacollection_id)
            return metacollection.item_set.all()

        return super().get_queryset()

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        return self.add_related_object_view(Item, 'item')

    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk=None):
        return self.remove_related_object_view('item')

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()
