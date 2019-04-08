# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import collection_devices as permissions


class CollectionDeviceViewSet(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              utils.CustomViewSetMixin,
                              GenericViewSet):
    queryset = models.CollectionDevice.objects.all() # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.data_collections.devices)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasUpdatePermission |
                IsAdmin
            ),
        ],
        utils.Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                IsAdmin
            ),
        ]
    })
