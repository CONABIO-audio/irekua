# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import LicenceTypeSerializer


# Create your views here.
class LicenceTypeViewSet(viewsets.ModelViewSet):
    queryset = db.LicenceType.objects.all()
    serializer_class = LicenceTypeSerializer
