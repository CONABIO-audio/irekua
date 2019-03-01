
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionDeviceSerializer


# Create your views here.
class CollectionDeviceViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionDevice.objects.all()
    serializer_class = CollectionDeviceSerializer
