# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

import database.models as db

from rest.serializers import sampling_events
from rest.serializers import items as item_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.filters import SamplingEventFilter

from .utils import AdditionalActionsMixin


class SamplingEventViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           SerializerMappingMixin,
                           AdditionalActionsMixin,
                           GenericViewSet):
    queryset = db.SamplingEvent.objects.all()
    search_fields = ('sampling_event_type__name',)
    filterset_class = SamplingEventFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(sampling_events)
        .extend(
            add_item=item_serializers.CreateSerializer,
            items=item_serializers.ListSerializer
        ))

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event = self.get_object()
        except AssertionError:
            sampling_event = None

        context['sampling_event'] = sampling_event
        return context

    @action(detail=True, methods=['POST'])
    def add_item(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        sampling_event = self.get_object()
        queryset = sampling_event.item_set.all()
        return self.list_related_object_view(queryset)
