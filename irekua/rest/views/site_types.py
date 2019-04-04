# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.filters import SiteTypeFilter


class SiteTypeViewSet(SerializerMappingMixin,
                      PermissionMappingMixin,
                      ModelViewSet):
    queryset = db.SiteType.objects.all()
    serializer_mapping = SerializerMapping.from_module(site_types)
    search_fields = ('name', )
    filterset_class = SiteTypeFilter

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
