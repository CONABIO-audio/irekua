# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import MetaCollectionSerializer


# Create your views here.
class MetaCollectionViewSet(viewsets.ModelViewSet):
    queryset = db.MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer
