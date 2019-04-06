# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import DeviceType

from rest.serializers.object_types import device_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.filters import DeviceTypeFilter


class DeviceTypeViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        SerializerMappingMixin,
                        GenericViewSet):
    queryset = DeviceType.objects.all()
    filterset_class = DeviceTypeFilter
    search_fields = ('name', )
    permission_classes = (IsAdmin | ReadOnly, )
    serializer_mapping = SerializerMapping.from_module(device_types)
