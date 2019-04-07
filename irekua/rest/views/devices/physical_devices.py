# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database.models import PhysicalDevice

from rest.serializers.devices import physical_devices

from rest.permissions import IsAdmin
from rest.permissions import physical_devices as permissions
from rest.permissions import ReadOnly

from rest.filters import PhysicalDeviceFilter

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class PhysicalDeviceViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):

    queryset = PhysicalDevice.objects.all()
    filterset_class = PhysicalDeviceFilter
    search_fields = ('device__brand__name', 'device__model')

    serializer_mapping = SerializerMapping.from_module(physical_devices)
    permission_mapping = PermissionMapping(
        default=permissions.IsOwner | IsAdmin | ReadOnly)
