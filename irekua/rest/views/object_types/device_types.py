# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import DeviceType

from rest.serializers.object_types import device_types

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class DeviceTypeViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        CustomViewSetMixin,
                        GenericViewSet):
    queryset = DeviceType.objects.all()

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
    serializer_mapping = SerializerMapping.from_module(device_types)
