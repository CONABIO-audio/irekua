# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionDevice

from rest.serializers.data_collections import collection_devices

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import collection_devices as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class CollectionDeviceViewSet(mixins.UpdateModelMixin,
                              mixins.RetrieveModelMixin,
                              mixins.DestroyModelMixin,
                              CustomViewSetMixin,
                              GenericViewSet):
    queryset = CollectionDevice.objects.all()
    serializer_mapping = SerializerMapping.from_module(collection_devices)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasUpdatePermission |
                IsAdmin
            ),
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsOwner |
                IsAdmin
            ),
        ]
    })
