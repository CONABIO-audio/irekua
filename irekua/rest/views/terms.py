# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import TermSerializer


# Create your views here.
class TermViewSet(viewsets.ModelViewSet):
    queryset = db.Term.objects.all()
    serializer_class = TermSerializer
