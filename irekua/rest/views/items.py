# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
import django_filters

import database.models as db
from rest.serializers import items
from rest.filters import BaseFilter
from .utils import NoCreateViewSet


class Filter(BaseFilter):
    is_uploaded = django_filters.BooleanFilter(
        field_name='item_file',
        method='is_uploaded_filter',
        label='is uploaded')

    def is_uploaded_filter(self, queryset, name, value):
        return queryset.filter(item_file__isnull=False)

    class Meta:
        model = db.Item
        fields = (
            'is_uploaded',
            'item_type__name',
            'sampling_event__sampling_event_type__name',
            'sampling_event__collection__name',
            'sampling_event__collection__collection_type',
            'sampling_event__site__site_type__name',
            'sampling_event__device__device__device_type__name',
            'sampling_event__device__device__brand__name',
        )


class ItemViewSet(NoCreateViewSet):
    query_is_open = (
        Q(licence__is_active=False) |
        Q(licence__licence_type__can_view=True)
    )
    queryset = db.Item.objects.filter(query_is_open)
    serializer_module = items
    filterset_class = Filter
    search_fields = ('item_type__name', )
