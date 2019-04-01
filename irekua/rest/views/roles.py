# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import roles
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import RoleFilter

from .utils import AdditionalActionsMixin


class RoleViewSet(SerializerMappingMixin,
                  AdditionalActionsMixin,
                  ModelViewSet):
    queryset = db.Role.objects.all()
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = RoleFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(roles)
        .extend(
            add_permission=roles.SelectPermissionSerializer,
            remove_permission=roles.SelectPermissionSerializer
        ))

    @action(detail=True, methods=['POST'])
    def add_permission(self, request, pk=None):
        return self.add_related_object_view(
            Permission,
            'permission')

    @action(detail=True, methods=['POST'])
    def remove_permission(self, request, pk=None):
        return self.remove_related_object_view(
            'permission')
