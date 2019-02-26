# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import AnnotationSerializer


# Create your views here.
class AnnotationViewSet(viewsets.ModelViewSet):
    queryset = db.Annotation.objects.all()
    serializer_class = AnnotationSerializer
