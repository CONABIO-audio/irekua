# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import MetaCollection
from database.models import Item

from rest.serializers import metacollections
from rest.serializers import items as item_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsSpecialUser
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated

from rest.filters import MetaCollectionFilter
from rest.utils import Actions

from .utils import AdditionalActionsMixin


class MetaCollectionViewSet(SerializerMappingMixin,
                            AdditionalActionsMixin,
                            PermissionMappingMixin,
                            ModelViewSet):
    queryset = MetaCollection.objects.all()
    filterset_class = MetaCollectionFilter
    search_fields = ('name', )

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

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        return self.add_related_object_view(
            Item,
            'item')

    @action(detail=True, methods=['POST'])
    def remove_item(self, request, pk=None):
        return self.remove_related_object_view(
            'item')

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        metacollection = self.get_object()
        queryset = metacollection.item_set.all()
        return self.list_related_object_view(queryset)
