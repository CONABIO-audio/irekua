# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SamplingEventTypeDeviceType

from rest.serializers.object_types.sampling_events import sampling_event_type_device_types

from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class SamplingEventTypeDeviceTypeViewSet(mixins.RetrieveModelMixin,
                                         mixins.DestroyModelMixin,
                                         CustomViewSetMixin,
                                         GenericViewSet):
    queryset = SamplingEventTypeDeviceType.objects.all()
    serializer_mapping = SerializerMapping.from_module(
        sampling_event_type_device_types)

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
