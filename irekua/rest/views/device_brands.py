# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db

from rest.serializers import device_brands
from rest.permissions import IsAdmin, IsCurator, ReadAndCreateOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.DeviceBrand
        fields = ('name', )


class DeviceBrandViewSet(BaseViewSet):
    queryset = db.DeviceBrand.objects.all()
    permission_classes = (IsAdmin | IsCurator | ReadAndCreateOnly, )
    search_fields = ('name', )
    filterset_class = Filter
    serializer_module = device_brands
