# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

import database.models as db

from rest.serializers.devices import physical_devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAdmin
from rest.permissions import IsOwner
from rest.permissions import IsAuthenticated

from rest.filters import PhysicalDeviceFilter
from rest.utils import Actions


class PhysicalDeviceViewSet(mixins.UpdateModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):

    queryset = db.PhysicalDevice.objects.all()
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = PhysicalDeviceFilter

    serializer_mapping = SerializerMapping.from_module(physical_devices)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated, IsOwner | IsAdmin
        ],
        Actions.DESTROY: [
            IsAuthenticated, IsOwner | IsAdmin
        ]
    }, default=IsAuthenticated)
