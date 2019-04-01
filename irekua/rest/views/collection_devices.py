# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from database.models import CollectionDevice

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest.serializers import collection_devices
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping


class CollectionDeviceViewSet(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              SerializerMappingMixin,
                              GenericViewSet):
    queryset = CollectionDevice.objects.all()
    serializer_mapping = SerializerMapping.from_module(collection_devices)
