# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import DeviceBrand

from rest.serializers.devices import device_brands

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class DeviceBrandViewSet(mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         CustomViewSetMixin,
                         GenericViewSet):
    queryset = DeviceBrand.objects.all()

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
    serializer_mapping = SerializerMapping.from_module(device_brands)
