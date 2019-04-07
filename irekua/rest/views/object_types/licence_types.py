# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import LicenceType

from rest.serializers.object_types import licence_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.utils import Actions
from rest.filters import LicenceTypeFilter


class LicenceTypeViewSet(mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         SerializerMappingMixin,
                         PermissionMappingMixin,
                         GenericViewSet):
    queryset = LicenceType.objects.all()
    filterset_class = LicenceTypeFilter
    search_fields = ('name', )

    serializer_mapping = SerializerMapping.from_module(licence_types)
    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
        Actions.UPDATE: [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)
