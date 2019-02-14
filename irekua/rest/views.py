# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from .serializers import ItemSerializer


# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = db.Item.objects.all()
    serializer_class = ItemSerializer
