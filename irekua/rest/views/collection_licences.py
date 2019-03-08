# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionLicenceSerializer


# Create your views here.
class CollectionLicenceViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionLicence.objects.all()
    serializer_class = CollectionLicenceSerializer
