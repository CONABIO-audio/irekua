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
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.filters import DeviceFilter
from rest.utils import Actions
from rest.views.utils import AdditionalActionsMixin


class DeviceViewSet(AdditionalActionsMixin,
                    SerializerMappingMixin,
                    PermissionMappingMixin,
                    ModelViewSet):
    queryset = Device.objects.all()
    search_fields = ('brand__name', 'model')
    filterset_class = DeviceFilter

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

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = DeviceType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def brands(self, request):
        queryset = DeviceBrand.objects.all()
        return self.list_related_object_view(queryset)

    @brands.mapping.post
    def add_brand(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def physical_devices(self, request):
        queryset = PhysicalDevice.objects.all()
        return self.list_related_object_view(queryset)

    @physical_devices.mapping.post
    def add_physical_device(self, request):
        return self.create_related_object_view()
