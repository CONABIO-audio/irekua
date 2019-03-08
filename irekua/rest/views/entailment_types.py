# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import EntailmentTypeSerializer


# Create your views here.
class EntailmentTypeViewSet(viewsets.ModelViewSet):
    queryset = db.EntailmentType.objects.all()
    serializer_class = EntailmentTypeSerializer
