# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import metacollections
from rest.serializers import items as item_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsDeveloper, IsModel, ReadOnly
from rest.filters import MetaCollectionFilter

from .utils import AdditionalActionsMixin


class MetaCollectionViewSet(SerializerMappingMixin,
                            AdditionalActionsMixin,
                            ModelViewSet):
    queryset = db.MetaCollection.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | IsModel | ReadOnly, )
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

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        return self.add_related_object_view(
            db.Item,
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
