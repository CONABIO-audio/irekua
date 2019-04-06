# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import DeviceBrand

from rest.serializers.devices import device_brands
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import ReadAndCreateOnly

from rest.filters import DeviceBrandFilter


class DeviceBrandViewSet(mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         SerializerMappingMixin,
                         GenericViewSet):
    queryset = DeviceBrand.objects.all()
    search_fields = ('name', )
    filterset_class = DeviceBrandFilter

    permission_classes = (IsAdmin | IsCurator | ReadAndCreateOnly, )
    serializer_mapping = SerializerMapping.from_module(device_brands)
