# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import sampling_event_types
from rest.serializers import device_types
from rest.serializers import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import SamplingEventTypeFilter

from .utils import AdditionalActionsMixin


class SamplingEventTypeViewSet(AdditionalActionsMixin,
                               SerializerMappingMixin,
                               ModelViewSet):
    queryset = db.SamplingEventType.objects.all()
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = SamplingEventTypeFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(sampling_event_types)
        .extend(
            add_device_types=device_types.SelectSerializer,
            remove_device_type=device_types.SelectSerializer,
            add_site_types=site_types.SelectSerializer,
            remove_site_type=site_types.SelectSerializer
        ))

    @action(detail=True, methods=['POST'])
    def add_device_types(self, request, pk=None):
        return self.add_related_object_view(
            db.DeviceType,
            'device_type')

    @action(detail=True, methods=['POST'])
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view(
            'device_type')

    @action(detail=True, methods=['POST'])
    def add_site_types(self, request, pk=None):
        return self.add_related_object_view(
            db.SiteType,
            'site_type')

    @action(detail=True, methods=['POST'])
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view(
            'site_type')
