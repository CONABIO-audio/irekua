# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import annotation_tools
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.AnnotationTool
        fields = (
            'name',
            'version')


class AnnotationToolViewSet(BaseViewSet):
    queryset = db.AnnotationTool.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
    serializer_module = annotation_tools
