# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import ItemType
from database.models import EventType

from rest.serializers.object_types import item_types
from rest.serializers.object_types import event_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly

from rest.filters import ItemTypeFilter
from rest.views.utils import AdditionalActionsMixin


class ItemTypeViewSet(SerializerMappingMixin,
                      AdditionalActionsMixin,
                      ModelViewSet):
    queryset = ItemType.objects.all()
    filterset_class = ItemTypeFilter
    search_fields = (
        'name',
        'media_type',
    )

    serializer_mapping = (
        SerializerMapping
        .from_module(item_types)
        .extend(
            add_event_types=event_types.SelectSerializer,
            remove_event_types=event_types.SelectSerializer
        ))
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )

    @action(detail=True, methods=['POST'])
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(
            EventType,
            'event_type')

    @action(detail=True, methods=['POST'])
    def remove_event_types(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')
