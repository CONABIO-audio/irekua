# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionDeviceTypeSerializer


# Create your views here.
class CollectionDeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionDeviceType.objects.all()
    serializer_class = CollectionDeviceTypeSerializer
