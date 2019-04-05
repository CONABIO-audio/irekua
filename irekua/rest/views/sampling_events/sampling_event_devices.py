# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SamplingEventDevice

from rest.serializers.sampling_events import sampling_event_devices
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest.utils import Actions


class SamplingEventDeviceViewSet(mixins.UpdateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.DestroyModelMixin,
                                 SerializerMappingMixin,
                                 PermissionMappingMixin,
                                 GenericViewSet):
    queryset = SamplingEventDevice.objects.all()
    serializer_mapping = SerializerMapping.from_module(sampling_event_devices)

    permission_mapping = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated
    }, default=[IsAuthenticated, IsAdmin])
