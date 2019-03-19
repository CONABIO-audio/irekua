# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import annotation_types
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.AnnotationType
        fields = ('name', )


class AnnotationTypeViewSet(BaseViewSet):
    queryset = db.AnnotationType.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
    serializer_module = annotation_types
