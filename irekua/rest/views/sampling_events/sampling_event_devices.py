# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database import models
from rest import serializers
from rest import filters
from rest import utils

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin


class SamplingEventDeviceViewSet(mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 utils.CustomViewSetMixin,
                                 GenericViewSet):
    queryset = models.SamplingEventDevice.objects.all()  # pylint: disable=E1101
    filterset_class = filters.sampling_event_devices.Filter
    search_fields = filters.sampling_event_devices.search_fields

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.sampling_events.devices)
        .extend(
            items=serializers.items.items.ListSerializer,
            add_item=serializers.items.items.CreateSerializer,
        ))

    permission_mapping = utils.PermissionMapping({
        utils.Actions.RETRIEVE: IsAuthenticated # TODO: Fix permissions
    }, default=[IsAuthenticated, IsAdmin])

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event_device = self.get_object()
        except (AttributeError, AssertionError):
            sampling_event_device = None

        context['sampling_event_device'] = sampling_event_device
        return context

    def get_queryset(self):
        if self.action == 'items':
            object_id = self.kwargs['pk']
            return models.Item.objects.filter(sampling_event_device=object_id)  # pylint: disable=E1101

        return super().get_queryset()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.items.Filter,
        search_fields=filters.items.search_fields)
    def items(self, request, pk=None):
        return self.list_related_object_view()

    @items.mapping.post
    def add_item(self, request, pk=None):
        self.create_related_object_view()
