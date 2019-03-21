# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db
from rest.serializers import sampling_event_types
from rest.serializers import device_types
from rest.serializers import site_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.SamplingEventType
        fields = (
            'name',
            'restrict_device_types',
            'restrict_site_types',
        )


class SamplingEventTypeViewSet(BaseViewSet, AdditionalActions):
    queryset = db.SamplingEventType.objects.all()
    serializer_module = sampling_event_types
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=device_types.SelectSerializer)
    def add_device_types(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=device_types.SelectSerializer)
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=site_types.SelectSerializer)
    def add_site_types(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=site_types.SelectSerializer)
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')
