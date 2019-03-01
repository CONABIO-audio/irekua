# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import AnnotationTypeSerializer


# Create your views here.
class AnnotationTypeViewSet(viewsets.ModelViewSet):
    queryset = db.AnnotationType.objects.all()
    serializer_class = AnnotationTypeSerializer
