# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database.models import ItemType
from database.models import EventType

from rest.serializers.object_types import item_types
from rest.serializers.object_types import event_types

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class ItemTypeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      CustomViewSetMixin,
                      GenericViewSet):
    queryset = ItemType.objects.all()

    serializer_mapping = (
        SerializerMapping
        .from_module(item_types)
        .extend(
            add_event_types=event_types.SelectSerializer,
            remove_event_types=event_types.SelectSerializer
        ))
    permission_classes = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated,
        Actions.DESTROY: IsAdmin,
    }, default=IsDeveloper | IsAdmin)

    @action(detail=True, methods=['POST'])
    def add_event_types(self, request, pk=None):
        return self.add_related_object_view(
            EventType,
            'event_type')

    @action(detail=True, methods=['POST'])
    def remove_event_types(self, request, pk=None):
        return self.remove_related_object_view(
            'event_type')
