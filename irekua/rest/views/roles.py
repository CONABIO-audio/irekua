# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import Permission
from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

import database.models as db
from rest.serializers.roles import RoleSerializer
from rest.permissions import IsAdmin, ReadOnly


class RolePermissionSerializer(serializers.Serializer):
    permissions = serializers.SlugRelatedField(
        many=False,
        write_only=True,
        queryset=Permission.objects.filter(content_type__app_label='database'),
        slug_field='codename')

    class Meta:
        model = db.Role
        fields = ('permissions', )


class RoleViewSet(viewsets.ModelViewSet):
    queryset = db.Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )

    @action(detail=True, methods=['POST'], serializer_class=RolePermissionSerializer)
    def add_permission(self, request, pk=None):
        try:
            role = db.Role.objects.get(pk=pk)
        except db.Role.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = RolePermissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            permission = Permission.objects.get(codename=serializer.initial_data['permissions'])
        except Permission.DoesNotExist:
            return Response('No such permission exists', status=status.HTTP_400_BAD_REQUEST)

        role.permissions.add(permission)
        return Response(status=status.HTTP_200_OK)
