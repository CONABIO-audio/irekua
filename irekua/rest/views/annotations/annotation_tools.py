# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import AnnotationTool

from rest.serializers.annotations import annotation_tools
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsDeveloper
from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest.filters import AnnotationToolFilter
from rest.utils import Actions


class AnnotationToolViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):
    queryset = AnnotationTool.objects.all()
    search_fields = ('name', )
    filterset_class = AnnotationToolFilter

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            IsDeveloper | IsAdmin,
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsDeveloper | IsAdmin,
        ]
    }, default=IsAuthenticated)
    serializer_mapping = SerializerMapping.from_module(annotation_tools)
