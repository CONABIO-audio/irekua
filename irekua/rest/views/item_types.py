# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db
from rest.serializers import item_types
from rest.serializers import event_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.ItemType
        fields = (
            'name',
            'media_type'
        )


class ItemTypeViewSet(BaseViewSet, AdditionalActions):
    queryset = db.ItemType.objects.all()
    serializer_module = item_types
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'media_type', )
    filterset_class = Filter

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=event_types.SelectSerializer)
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(
            db.EventType,
            'event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=event_types.SelectSerializer)
    def remove_event_types(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=event_types.CreateSerializer)
    def create_event_type(self, request, pk=None):
        return self.create_related_object_view(
            db.EventType,
            'event_type')
