# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import AnnotationToolSerializer


# Create your views here.
class AnnotationToolViewSet(viewsets.ModelViewSet):
    queryset = db.AnnotationTool.objects.all()
    serializer_class = AnnotationToolSerializer
