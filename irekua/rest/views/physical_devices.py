# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import physical_devices
from rest.permissions import IsAdmin, IsOwner, ListAndCreateOnly


class PhysicalDeviceViewSet(viewsets.ModelViewSet):
    queryset = db.PhysicalDevice.objects.all()
    serializer_class = physical_devices.CreateSerializer
    permission_classes = (IsAdmin | IsOwner | ListAndCreateOnly, )
    search_fields = ('device__brand__name', 'device__model')
    filter_fields = (
        'device__brand__name',
        'device__model',
        'device__device_type__name',
        'owner__username',
        'owner__first_name'
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return physical_devices.ListSerializer
        if self.action == 'retrieve':
            return physical_devices.DetailSerializer

        return super().get_serializer_class()
