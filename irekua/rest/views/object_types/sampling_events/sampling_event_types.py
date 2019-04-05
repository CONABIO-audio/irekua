# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import SamplingEventType

from rest.serializers.object_types.sampling_events import sampling_event_types
from rest.serializers.object_types.sampling_events import sampling_event_type_device_types
from rest.serializers.object_types.sampling_events import sampling_event_type_site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.filters import SamplingEventTypeFilter
from rest.views.utils import AdditionalActionsMixin


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
            device_types=sampling_event_type_device_types.ListSerializer,
            add_device_types=sampling_event_type_device_types.CreateSerializer,
            site_types=sampling_event_type_site_types.ListSerializer,
            add_site_types=sampling_event_type_site_types.CreateSerializer,
        ))
    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event_type = self.get_object()
        except (AttributeError, AssertionError):
            sampling_event_type = None

        context['sampling_event_type'] = sampling_event_type
        return context

    @action(detail=True, methods=['GET'])
    def device_types(self, request, pk=None):
        sampling_event_type = self.get_object()
        queryset = sampling_event_type.samplingeventtypedevicetype_set.all()
        return self.list_related_object_view(queryset)

    @device_types.mapping.post
    def add_device_types(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def site_types(self, request, pk=None):
        model = SamplingEventType.site_types.through
        sampling_event_type_id = self.kwargs['pk']
        queryset = model.objects.filter(
            samplingeventtype_id=sampling_event_type_id)
        return self.list_related_object_view(queryset)

    @site_types.mapping.post
    def add_site_types(self, request, pk=None):
        return self.create_related_object_view()
