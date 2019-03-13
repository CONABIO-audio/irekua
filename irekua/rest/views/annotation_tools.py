# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import AnnotationToolSerializer
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly


class AnnotationToolViewSet(ModelViewSet):
    queryset = db.AnnotationTool.objects.all()
    serializer_class = AnnotationToolSerializer
    permission_classes = (IsAdmin|IsDeveloper|ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', 'version', )
