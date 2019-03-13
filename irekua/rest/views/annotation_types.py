# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import AnnotationTypeSerializer
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly


class AnnotationTypeViewSet(ModelViewSet):
    queryset = db.AnnotationType.objects.all()
    serializer_class = AnnotationTypeSerializer
    permission_classes = (IsAdmin|IsDeveloper|ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )
