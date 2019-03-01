# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SecondaryItemSerializer


# Create your views here.
class SecondaryItemViewSet(viewsets.ModelViewSet):
    queryset = db.SecondaryItem.objects.all()
    serializer_class = SecondaryItemSerializer
