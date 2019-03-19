# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import devices
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Device
        fields = (
            'brand__name',
            'model',
            'device_type__name',
        )


class DeviceViewSet(BaseViewSet):
    queryset = db.Device.objects.all()
    serializer_module = devices
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
    search_fields = ('brand__name', 'model')
    filterset_class = Filter
