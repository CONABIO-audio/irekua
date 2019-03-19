# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import site_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.SiteType
        fields = ('name', )


class SiteTypeViewSet(BaseViewSet):
    queryset = db.SiteType.objects.all()
    serializer_module = site_types
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
