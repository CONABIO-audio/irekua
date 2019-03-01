# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import PhysicalDeviceSerializer


# Create your views here.
class PhysicalDeviceViewSet(viewsets.ModelViewSet):
    queryset = db.PhysicalDevice.objects.all()
    serializer_class = PhysicalDeviceSerializer
