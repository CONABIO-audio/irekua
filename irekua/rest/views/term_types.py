# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import TermTypeSerializer


# Create your views here.
class TermTypeViewSet(viewsets.ModelViewSet):
    queryset = db.TermType.objects.all()
    serializer_class = TermTypeSerializer
