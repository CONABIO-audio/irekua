# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import device_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import DeviceTypeFilter


class DeviceTypeViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.DeviceType.objects.all()
    serializer_mapping = SerializerMapping.from_module(device_types)
    permission_classes = (IsAdmin | ReadOnly, )
    filterset_class = DeviceTypeFilter
    search_fields = ('name', )
