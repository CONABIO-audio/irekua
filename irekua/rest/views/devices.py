# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import DeviceFilter


class DeviceViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Device.objects.all()
    serializer_mapping = SerializerMapping.from_module(devices)
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
    search_fields = ('brand__name', 'model')
    filterset_class = DeviceFilter
