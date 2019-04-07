# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from database.models import Device
from database.models import PhysicalDevice
from database.models import DeviceType
from database.models import DeviceBrand

from rest.serializers.object_types import device_types
from rest.serializers.devices import devices
from rest.serializers.devices import device_brands
from rest.serializers.devices import physical_devices as physical_device_serializers

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest import filters

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class DeviceViewSet(CustomViewSetMixin, ModelViewSet):
    queryset = Device.objects.all()
    filterset_class = filters.devices.Filter
    search_fields = filters.devices.search_fields

    serializer_mapping = (
        SerializerMapping
        .from_module(devices)
        .extend(
            types=device_types.ListSerializer,
            add_type=device_types.CreateSerializer,
            brands=device_brands.ListSerializer,
            add_brand=device_brands.CreateSerializer,
            physical_devices=physical_device_serializers.ListSerializer,
            add_physical_device=physical_device_serializers.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.UPDATE: IsAdmin,
        Actions.DESTROY: IsAdmin,
        'add_type': IsAdmin,
    }, default=IsAuthenticated)

    def get_queryset(self):
        if self.action == 'types':
            return DeviceType.objects.all()

        if self.action == 'brands':
            return DeviceBrand.objects.all()

        if self.action == 'physical_devices':
            return PhysicalDevice.objects.all() # TODO: set adequate queryset for user

        return super().get_queryset()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.device_types.Filter,
        search_fields=filters.device_types.search_fields)
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.device_brands.Filter,
        search_fields=filters.device_brands.search_fields)
    def brands(self, request):
        return self.list_related_object_view()

    @brands.mapping.post
    def add_brand(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.physical_devices.Filter,
        search_fields=filters.physical_devices.search_fields)
    def physical_devices(self, request):
        return self.list_related_object_view()

    @physical_devices.mapping.post
    def add_physical_device(self, request):
        return self.create_related_object_view()
