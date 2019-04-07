# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database.models import Role

from rest.serializers.users import roles

from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class RoleViewSet(mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  CustomViewSetMixin,
                  GenericViewSet):
    queryset = Role.objects.all()

    serializer_mapping = (
        SerializerMapping
        .from_module(roles)
        .extend(
            add_permission=roles.SelectPermissionSerializer,
            remove_permission=roles.SelectPermissionSerializer
        ))
    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)

    @action(detail=True, methods=['POST'])
    def add_permission(self, request, pk=None):
        return self.add_related_object_view(
            Permission, 'permission')

    @action(detail=True, methods=['POST'])
    def remove_permission(self, request, pk=None):
        return self.remove_related_object_view(
            'permission')
