# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SiteType

from rest.serializers.object_types import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest.utils import Actions
from rest.filters import SiteTypeFilter


class SiteTypeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      SerializerMappingMixin,
                      PermissionMappingMixin,
                      GenericViewSet):
    queryset = SiteType.objects.all()
    search_fields = ('name', )
    filterset_class = SiteTypeFilter

    serializer_mapping = SerializerMapping.from_module(site_types)
    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated | IsAdmin],
        Actions.UPDATE: [IsAuthenticated | IsAdmin],
    }, default=IsAuthenticated)
