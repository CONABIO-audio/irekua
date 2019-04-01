# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import item_types
from rest.serializers import event_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import ItemTypeFilter
from .utils import AdditionalActionsMixin


class ItemTypeViewSet(SerializerMappingMixin,
                      AdditionalActionsMixin,
                      ModelViewSet):
    queryset = db.ItemType.objects.all()
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'media_type', )
    filterset_class = ItemTypeFilter
    serializer_mapping = (
        SerializerMapping
        .from_module(item_types)
        .extend(
            add_event_types=event_types.SelectSerializer,
            remove_event_types=event_types.SelectSerializer
        ))

    @action(detail=True, methods=['POST'])
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(
            db.EventType,
            'event_type')

    @action(detail=True, methods=['POST'])
    def remove_event_types(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')
