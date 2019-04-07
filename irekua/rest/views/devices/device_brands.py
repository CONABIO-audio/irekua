# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import DeviceBrand

from rest.serializers.devices import device_brands
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.filters import DeviceBrandFilter
from rest.utils import Actions


class DeviceBrandViewSet(mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         SerializerMappingMixin,
                         PermissionMappingMixin,
                         GenericViewSet):
    queryset = DeviceBrand.objects.all()
    search_fields = ('name', )
    filterset_class = DeviceBrandFilter

    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
        Actions.UPDATE: [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)
    serializer_mapping = SerializerMapping.from_module(device_brands)
