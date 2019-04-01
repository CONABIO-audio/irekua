# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import annotation_tools
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import AnnotationToolFilter


class AnnotationToolViewSet(SerializerMappingMixin,
                            PermissionMappingMixin,
                            ModelViewSet):
    queryset = db.AnnotationTool.objects.all()
    search_fields = ('name', )
    filterset_class = AnnotationToolFilter

    permission_mapping = PermissionMapping(
        default=IsAdmin | IsDeveloper | ReadOnly)
    serializer_mapping = SerializerMapping.from_module(annotation_tools)
