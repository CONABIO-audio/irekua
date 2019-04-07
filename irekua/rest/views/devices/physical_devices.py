# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database.models import PhysicalDevice

from rest.serializers.devices import physical_devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAdmin
from rest.permissions import physical_devices as permissions
from rest.permissions import IsAuthenticated

from rest.filters import PhysicalDeviceFilter
from rest.utils import Actions


class PhysicalDeviceViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):

    queryset = PhysicalDevice.objects.all()
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = PhysicalDeviceFilter

    serializer_mapping = SerializerMapping.from_module(physical_devices)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsOwner | IsAdmin
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsOwner | IsAdmin
        ]
    }, default=IsAuthenticated)
