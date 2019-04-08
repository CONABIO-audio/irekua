# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database import models
from rest import utils
from rest import serializers

from rest.permissions import IsAdmin
from rest.permissions import physical_devices as permissions
from rest.permissions import ReadOnly


class PhysicalDeviceViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):

    queryset = models.PhysicalDevice.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.devices.physical_devices)
    permission_mapping = utils.PermissionMapping(
        default=permissions.IsOwner | IsAdmin | ReadOnly)
