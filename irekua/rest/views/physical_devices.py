# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import physical_devices
from rest.serializers import collection_devices
from rest.permissions import IsAdmin, IsOwner, ListAndCreateOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.PhysicalDevice
        fields = (
            'device__brand__name',
            'device__model',
            'device__device_type__name',
            'owner__username',
            'owner__first_name'
        )


class PhysicalDeviceViewSet(BaseViewSet):
    queryset = db.PhysicalDevice.objects.all()
    serializer_module = physical_devices
    permission_classes = (IsAdmin | IsOwner | ListAndCreateOnly, )
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = Filter


class CollectionDeviceViewSet(BaseViewSet):
    serializer_module = collection_devices
    search_fields = ('device__brand__name', 'device__model')
    filterset_class = Filter

    def get_queryset(self):
        collection = self.kwargs['collection_pk']
        return db.CollectionDevice.objects.filter(collection=collection)
