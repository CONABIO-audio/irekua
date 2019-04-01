# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import device_brands
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping
from rest.permissions import IsAdmin, IsCurator, ReadAndCreateOnly
from rest.filters import DeviceBrandFilter


class DeviceBrandViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.DeviceBrand.objects.all()
    permission_classes = (IsAdmin | IsCurator | ReadAndCreateOnly, )
    search_fields = ('name', )
    filterset_class = DeviceBrandFilter
    serializer_mapping = SerializerMapping.from_module(device_brands)
