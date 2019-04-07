# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import SamplingEventDevice

from rest.serializers.sampling_events import sampling_event_devices
from rest.serializers.items import items as item_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest.utils import Actions
from rest.views.utils import AdditionalActionsMixin


class SamplingEventDeviceViewSet(mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 SerializerMappingMixin,
                                 AdditionalActionsMixin,
                                 PermissionMappingMixin,
                                 GenericViewSet):
    queryset = SamplingEventDevice.objects.all()

    serializer_mapping = (
        SerializerMapping
        .from_module(sampling_event_devices)
        .extend(
            items=item_serializers.ListSerializer,
            add_item=item_serializers.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated
    }, default=[IsAuthenticated, IsAdmin])

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event_device = self.get_object()
        except (AttributeError, AssertionError):
            sampling_event_device = None

        context['sampling_event_device'] = sampling_event_device
        return context

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        sampling_event_device = self.get_object()
        queryset = sampling_event_device.item_set.all()
        return self.list_related_object_view(queryset)

    @items.mapping.post
    def add_item(self, request, pk=None):
        self.create_related_object_view()
