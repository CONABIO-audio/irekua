# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import SamplingEventType
from database.models import DeviceType
from database.models import SiteType

from rest.serializers import sampling_event_types
from rest.serializers import device_types
from rest.serializers import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.filters import SamplingEventTypeFilter

from .utils import AdditionalActionsMixin


class SamplingEventTypeViewSet(AdditionalActionsMixin,
                               SerializerMappingMixin,
                               PermissionMappingMixin,
                               ModelViewSet):
    queryset = SamplingEventType.objects.all()
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
    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)

    @action(detail=True, methods=['POST'])
    def add_device_types(self, request, pk=None):
        return self.add_related_object_view(
            DeviceType, 'device_type')

    @action(detail=True, methods=['POST'])
    def remove_device_type(self, request, pk=None):
        return self.remove_related_object_view('device_type')

    @action(detail=True, methods=['POST'])
    def add_site_types(self, request, pk=None):
        return self.add_related_object_view(
            SiteType, 'site_type')

    @action(detail=True, methods=['POST'])
    def remove_site_type(self, request, pk=None):
        return self.remove_related_object_view('site_type')
