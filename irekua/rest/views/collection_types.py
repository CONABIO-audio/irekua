# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionTypeSerializer


# Create your views here.
class CollectionTypeViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionType.objects.all()
    serializer_class = CollectionTypeSerializer
