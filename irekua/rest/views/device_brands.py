# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import DeviceBrandSerializer


# Create your views here.
class DeviceBrandViewSet(viewsets.ModelViewSet):
    queryset = db.DeviceBrand.objects.all()
    serializer_class = DeviceBrandSerializer
