# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import LicenceSerializer


# Create your views here.
class LicenceViewSet(viewsets.ModelViewSet):
    queryset = db.Licence.objects.all()
    serializer_class = LicenceSerializer
