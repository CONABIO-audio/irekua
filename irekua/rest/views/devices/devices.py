# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import Device

from rest.serializers.devices import devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import ReadAndCreateOnly

from rest.filters import DeviceFilter


class DeviceViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = Device.objects.all()
    search_fields = ('brand__name', 'model')
    filterset_class = DeviceFilter
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
    serializer_mapping = SerializerMapping.from_module(devices)
