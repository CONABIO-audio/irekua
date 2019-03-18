# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import action

import database.models as db
from rest.serializers import sampling_event_types
from rest.permissions import IsAdmin, ReadOnly
from .utils import AdditionalActions


class SamplingEventTypeViewSet(viewsets.ModelViewSet, AdditionalActions):
    queryset = db.SamplingEventType.objects.all()
    serializer_class = sampling_event_types.CreateSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filter_fields = (
        'name',
        'restrict_device_types',
        'restrict_site_types')

    def get_serializer_class(self):
        if self.action == 'list':
            return sampling_event_types.ListSerializer
        if self.action == 'retrieve':
            return sampling_event_types.DetailSerializer

        return super().get_serializer_class()

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.DeviceTypeSerializer)
    def add_device_types(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.DeviceTypeSerializer)
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.SiteTypeSerializer)
    def add_site_types(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=sampling_event_types.SiteTypeSerializer)
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')
