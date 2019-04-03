# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import annotation_types
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly

from rest.filters import AnnotationTypeFilter


class AnnotationTypeViewSet(SerializerMappingMixin,
                            PermissionMappingMixin,
                            ModelViewSet):
    queryset = db.AnnotationType.objects.all()
    search_fields = ('name', )
    filterset_class = AnnotationTypeFilter

    permission_mapping = PermissionMapping(
        default=IsAdmin | IsDeveloper | ReadOnly)
    serializer_mapping = SerializerMapping.from_module(annotation_types)
