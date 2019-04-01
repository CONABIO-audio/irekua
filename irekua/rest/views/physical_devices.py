# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import physical_devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsOwner, ListAndCreateOnly
from rest.filters import PhysicalDeviceFilter


class PhysicalDeviceViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.PhysicalDevice.objects.all()
    serializer_mapping = SerializerMapping.from_module(physical_devices)
    permission_classes = (IsAdmin | IsOwner | ListAndCreateOnly, )
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = PhysicalDeviceFilter
