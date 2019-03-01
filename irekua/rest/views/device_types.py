# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import DeviceTypeSerializer


# Create your views here.
class DeviceTypeViewSet(viewsets.ModelViewSet):
    queryset = db.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
