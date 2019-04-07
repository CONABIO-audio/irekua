# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database.models import EventType
from database.models import TermType

from rest.serializers.object_types import event_types
from rest.serializers.object_types import term_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.filters import EventTypeFilter
from rest.utils import Actions
from rest.views.utils import AdditionalActionsMixin


class EventTypeViewSet(mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       SerializerMappingMixin,
                       AdditionalActionsMixin,
                       PermissionMappingMixin,
                       GenericViewSet):
    queryset = EventType.objects.all()
    filterset_class = EventTypeFilter
    search_fields = ('name', )

    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
        Actions.UPDATE: [IsAuthenticated, IsDeveloper | IsAdmin],
    }, default=IsAuthenticated)
    serializer_mapping = (
        SerializerMapping
        .from_module(event_types)
        .extend(
            add_term_types=term_types.SelectSerializer,
            remove_term_types=term_types.SelectSerializer,
        ))

    @action(detail=True, methods=['POST'])
    def add_term_types(self, request, pk=None):
        return self.add_related_object_view(
            TermType,
            'term_type')

    @action(detail=True, methods=['POST'])
    def remove_term_types(self, request, pk=None):
        return self.remove_related_object_view(
            'term_type')
