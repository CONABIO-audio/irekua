# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils


class SamplingEventTypeViewSet(mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               utils.CustomViewSetMixin,
                               GenericViewSet):
    queryset = models.SamplingEventType.objects.all()  # pylint: disable=E1101

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.sampling_events.types)
        .extend(
            device_types=serializers.object_types.sampling_events.devices.ListSerializer,
            add_device_types=serializers.object_types.sampling_events.devices.CreateSerializer,
            site_types=serializers.object_types.sampling_events.sites.ListSerializer,
            add_site_types=serializers.object_types.sampling_events.sites.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event_type = self.get_object()
        except (AttributeError, AssertionError):
            sampling_event_type = None

        context['sampling_event_type'] = sampling_event_type
        return context

    def get_queryset(self):
        if self.action == 'device_types':
            sampling_event_type_id = self.kwargs['pk']
            queryset = (
                models.SamplingEventTypeDeviceTypeViewSet  # pylint: disable=E1101
                .objects
                .filter(sampling_event_type=sampling_event_type_id))
            return queryset

        if self.action == 'site_types':
            model = models.SamplingEventType.site_types.through  # pylint: disable=E1101
            sampling_event_type_id = self.kwargs['pk']
            return model.objects.filter(
                samplingeventtype_id=sampling_event_type_id)

        return super().get_queryset()

    @action(detail=True, methods=['GET'])
    def device_types(self, request, pk=None):
        return self.list_related_object_view()

    @device_types.mapping.post
    def add_device_types(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def site_types(self, request, pk=None):
        return self.list_related_object_view()

    @site_types.mapping.post
    def add_site_types(self, request, pk=None):
        return self.create_related_object_view()
