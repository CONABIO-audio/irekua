# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db
from rest.serializers import event_types, term_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.EventType
        fields = ('name', )


class EventTypeViewSet(BaseViewSet, AdditionalActions):
    queryset = db.EventType.objects.all()
    serializer_module = event_types
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=term_types.SelectSerializer)
    def add_label_types(self, request, pk=None):
        return self.add_related_object_view(
            db.TermType,
            'term_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=term_types.SelectSerializer)
    def remove_label_types(self, request, pk=None):
        return self.remove_related_object_view(
            'term_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=term_types.CreateSerializer)
    def create_label_type(self, request, pk=None):
        return self.create_related_object_view(
            db.TermType,
            'term_type')
