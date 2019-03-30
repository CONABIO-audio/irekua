# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import collection_devices
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.CollectionDevice
        fields = (
            'device__device__brand__name',
            'device__device__model',
            'device__device__device_type__name',
            'device__owner__username',
            'device__owner__first_name'
        )


class CollectionDeviceViewSet(BaseViewSet):
    queryset = db.CollectionDevice.objects.all()
    serializer_module = collection_devices
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = Filter
