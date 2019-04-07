# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database.models import EventType
from database.models import TermType

from rest.serializers.object_types import event_types
from rest.serializers.object_types import term_types

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class EventTypeViewSet(mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       CustomViewSetMixin,
                       GenericViewSet):
    queryset = EventType.objects.all()

    permission_mapping = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated,
        Actions.UPDATE: [
            IsAuthenticated,
            IsDeveloper | IsAdmin
        ],
    }, default=IsDeveloper | IsAdmin)

    serializer_mapping = (
        SerializerMapping
        .from_module(event_types)
        .extend(
            add_term_types=term_types.SelectSerializer,
            remove_term_types=term_types.SelectSerializer,
        ))

    @action(detail=True, methods=['POST'])
    def add_term_types(self, request, pk=None):
        return self.add_related_object_view(TermType, 'term_type')

    @action(detail=True, methods=['POST'])
    def remove_term_types(self, request, pk=None):
        return self.remove_related_object_view('term_type')
