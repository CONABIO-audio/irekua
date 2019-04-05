# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers.object_types import event_types
from rest.serializers.object_types import term_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly

from rest.filters import EventTypeFilter

from rest.views.utils import AdditionalActionsMixin


class EventTypeViewSet(SerializerMappingMixin,
                       AdditionalActionsMixin,
                       ModelViewSet):
    queryset = db.EventType.objects.all()
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = EventTypeFilter
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
            db.TermType,
            'term_type')

    @action(detail=True, methods=['POST'])
    def remove_term_types(self, request, pk=None):
        return self.remove_related_object_view(
            'term_type')
