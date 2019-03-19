# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

import database.models as db
from rest.serializers import sampling_events
from rest.filters import BaseFilter
from .utils import NoCreateViewSet


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


class SamplingEventViewSet(NoCreateViewSet):
    queryset = db.SamplingEvent.objects.all()
    serializer_module = sampling_events
    search_fields = ('sampling_event_type__name',)
    filterset_class = Filter
