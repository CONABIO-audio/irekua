# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework.decorators import action

import database.models as db
from rest.serializers import roles
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.Role
        fields = (
            'name',
        )


class RoleViewSet(BaseViewSet, AdditionalActions):
    queryset = db.Role.objects.all()
    serializer_module = roles
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=roles.SelectPermissionSerializer)
    def add_permission(self, request, pk=None):
        return self.add_related_object_view(
            Permission,
            'permission')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=roles.SelectPermissionSerializer)
    def remove_permission(self, request, pk=None):
        return self.remove_related_object_view(
            'permission')
