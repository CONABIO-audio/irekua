# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import DeviceSerializer
from rest.permissions import IsAdmin, ReadAndCreateOnly


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = db.Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
    search_fields = ('brand__name', 'model')
    filter_fields = (
        'brand__name',
        'model',
        'device_type__name'
    )
