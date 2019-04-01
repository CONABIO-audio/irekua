# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import SiteTypeFilter


class SiteTypeViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.SiteType.objects.all()
    serializer_mapping = SerializerMapping.from_module(site_types)
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = SiteTypeFilter
