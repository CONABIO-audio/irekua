# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import ItemTypeSerializer


# Create your views here.
class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = db.ItemType.objects.all()
    serializer_class = ItemTypeSerializer
