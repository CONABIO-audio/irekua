# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import CollectionUser

from rest.serializers import collection_users
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.utils import Actions

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import collection_users as permissions

from .utils import AdditionalActionsMixin


class CollectionUserViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            AdditionalActionsMixin,
                            GenericViewSet):
    queryset = CollectionUser.objects.all()

    serializer_mapping = (
        SerializerMapping
        .from_module(collection_users)
        .extend(
            change_admin_status=collection_users.AdminSerializer
        ))

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                permissions.HasUpdatePermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            ),
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                permissions.IsInCollection |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsSelf |
                IsAdmin
            ),
        ],
        'change_admin_status': [
            (
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsAdmin
            )
        ],
    })

    @action(detail=True, methods=['POST'])
    def change_admin_status(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
