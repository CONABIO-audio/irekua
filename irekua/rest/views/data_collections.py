
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionSerializer


# Create your views here.
class CollectionViewSet(viewsets.ModelViewSet):
    queryset = db.Collection.objects.all()
    serializer_class = CollectionSerializer
