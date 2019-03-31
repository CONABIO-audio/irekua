# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters
from rest_framework.decorators import action

import database.models as db
from rest.serializers import sampling_events
from rest.serializers import items as item_serializers
from rest.filters import BaseFilter
from .utils import NoCreateViewSet, AdditionalActions


class Filter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='site.latitude',
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='site.latitude',
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='site.longitude',
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='site.longitude',
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='site.altitude',
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='site.altitude',
        lookup_expr='lt')

    started_on__gt = django_filters.NumberFilter(
        field_name='started_on',
        lookup_expr='gt')
    started_on__lt = django_filters.NumberFilter(
        field_name='started_on',
        lookup_expr='lt')

    ended_on__gt = django_filters.NumberFilter(
        field_name='ended_on',
        lookup_expr='gt')
    ended_on__lt = django_filters.NumberFilter(
        field_name='ended_on',
        lookup_expr='lt')

    class Meta:
        model = db.SamplingEvent
        fields = (
            'sampling_event_type__name',
            'site__site_type__name',
            'site__locality',
            'device__device__device_type__name',
            'device__device__brand__name',
            'device__device__model',
            'collection__collection_type__name',
            'collection__name',
        )


class SamplingEventViewSet(NoCreateViewSet, AdditionalActions):
    queryset = db.SamplingEvent.objects.all()
    serializer_module = sampling_events
    search_fields = ('sampling_event_type__name',)
    filterset_class = Filter

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event = self.get_object()
        except AssertionError:
            sampling_event = None

        context['sampling_event'] = sampling_event
        return context

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=item_serializers.CreateSerializer)
    def add_item(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=True,
        methods=['GET'],
        serializer_class=item_serializers.ListSerializer)
    def items(self, request, pk=None):
        sampling_event = self.get_object()
        queryset = sampling_event.item_set.all()
        return self.list_related_object_view(queryset)
