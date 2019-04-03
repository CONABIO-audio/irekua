# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionSite

from rest.serializers import sites
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.utils import Actions

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import collection_sites as permissions


class CollectionSiteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):
    queryset = CollectionSite.objects.all()

    serializer_mapping = SerializerMapping.from_module(sites)

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasUpdatePermission |
                IsAdmin
            ),
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            ),
        ]
    })
