# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from rest.serializers import AnnotationToolSerializer


class AnnotationToolViewSet(viewsets.ModelViewSet):
    queryset = db.AnnotationTool.objects.all()
    serializer_class = AnnotationToolSerializer

    def get_permissions(self):
        if self.action in ['list', 'detail']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
