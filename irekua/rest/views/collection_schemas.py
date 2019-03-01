
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionSchemaSerializer


# Create your views here.
class CollectionSchemaViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionSchema.objects.all()
    serializer_class = CollectionSchemaSerializer
