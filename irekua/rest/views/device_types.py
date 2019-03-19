# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import device_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.DeviceType
        fields = ('name', )


class DeviceTypeViewSet(BaseViewSet):
    queryset = db.DeviceType.objects.all()
    serializer_module = device_types
    permission_classes = (IsAdmin | ReadOnly, )
    filterset_class = Filter
    search_fields = ('name', )
