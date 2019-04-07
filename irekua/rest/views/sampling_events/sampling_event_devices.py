# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import SamplingEventDevice
from database.models import Item

from rest.serializers.sampling_events import sampling_event_devices
from rest.serializers.items import items as item_serializers

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest import filters

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class SamplingEventDeviceViewSet(mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 CustomViewSetMixin,
                                 GenericViewSet):
    queryset = SamplingEventDevice.objects.all()
    filterset_class = filters.sampling_event_devices.Filter
    search_fields = filters.sampling_event_devices.search_fields

    serializer_mapping = (
        SerializerMapping
        .from_module(sampling_event_devices)
        .extend(
            items=item_serializers.ListSerializer,
            add_item=item_serializers.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated # TODO: Fix permissions
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
            return Item.objects.filter(sampling_event_device=object_id)

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
