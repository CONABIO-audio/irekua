# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils


class DeviceTypeViewSet(mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        utils.CustomViewSetMixin,
                        GenericViewSet):
    queryset = models.DeviceType.objects.all()  # pylint: disable=E1101

    permission_mapping = utils.PermissionMapping()
    
    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.object_types.devices)
