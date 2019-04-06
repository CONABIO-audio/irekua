# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import SamplingEvent
from database.models import Item

from rest.serializers.sampling_events import sampling_events
from rest.serializers.sampling_events import sampling_event_devices
from rest.serializers.items import items as item_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
import rest.permissions.sampling_events as permissions

from rest.filters import SamplingEventFilter
from rest.utils import Actions
from rest.views.utils import AdditionalActionsMixin


class SamplingEventViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           SerializerMappingMixin,
                           AdditionalActionsMixin,
                           PermissionMappingMixin,
                           GenericViewSet):
    queryset = SamplingEvent.objects.all()
    search_fields = ('sampling_event_type__name',)
    filterset_class = SamplingEventFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(sampling_events)
        .extend(
            items=item_serializers.ListSerializer,
            devices=sampling_event_devices.ListSerializer,
            add_device=sampling_event_devices.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasChangePermissions |
                IsAdmin
            )
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermissions |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        Actions.LIST: [
            IsAuthenticated,
        ],
        'items': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewItemsPermissions |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
    })

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            sampling_event = self.get_object()
        except (AssertionError, AttributeError):
            sampling_event = None

        context['sampling_event'] = sampling_event
        return context

    @action(detail=True, methods=['GET'])
    def devices(self, request, pk=None):
        sampling_event = self.get_object()
        queryset = sampling_event.samplingeventdevice_set.all()
        return self.list_related_object_view(queryset)

    @devices.mapping.post
    def add_device(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        queryset = Item.objects.filter(
            sampling_event_device__sampling_event=self.kwargs['pk']
        )
        return self.list_related_object_view(queryset)
