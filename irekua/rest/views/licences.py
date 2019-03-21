# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django_filters

import database.models as db
from rest.serializers import licences
from .utils import NoCreateViewSet


class Filter(django_filters.FilterSet):
    created_on__lt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='lt')
    created_on__gt = django_filters.DateTimeFilter(
        field_name='created_on',
        lookup_expr='gt')

    class Meta:
        model = db.Licence
        fields = (
            'licence_type__name',
            'signed_by__username',
            'signed_by__first_name',
            'collection__name',
        )


class LicenceViewSet(NoCreateViewSet):
    queryset = db.Licence.objects.all()
    serializer_module = licences
    filterset_class = Filter
