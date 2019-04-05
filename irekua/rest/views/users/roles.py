# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from database.models import Role

from rest.serializers.users import roles
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.filters import RoleFilter
from rest.views.utils import AdditionalActionsMixin


class RoleViewSet(SerializerMappingMixin,
                  AdditionalActionsMixin,
                  PermissionMappingMixin,
                  ModelViewSet):
    queryset = Role.objects.all()
    search_fields = ('name', )
    filterset_class = RoleFilter

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
