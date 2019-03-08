# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionItemTypeSerializer


# Create your views here.
class CollectionItemTypeViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionItemType.objects.all()
    serializer_class = CollectionItemTypeSerializer
