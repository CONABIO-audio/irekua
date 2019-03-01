# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import InstitutionSerializer


# Create your views here.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = db.Institution.objects.all()
    serializer_class = InstitutionSerializer
