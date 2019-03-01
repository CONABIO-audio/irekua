# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SchemaSerializer


# Create your views here.
class SchemaViewSet(viewsets.ModelViewSet):
    queryset = db.Schema.objects.all()
    serializer_class = SchemaSerializer
