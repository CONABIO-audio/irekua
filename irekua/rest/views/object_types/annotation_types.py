# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import AnnotationType

from rest.serializers.object_types import annotation_types
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsDeveloper
from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest.utils import Actions
from rest.filters import AnnotationTypeFilter


class AnnotationTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):
    queryset = AnnotationType.objects.all()
    filterset_class = AnnotationTypeFilter
    search_fields = ('name', )

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            IsDeveloper | IsAdmin,
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin,
        ],
    }, default=IsAuthenticated)
    serializer_mapping = SerializerMapping.from_module(annotation_types)
