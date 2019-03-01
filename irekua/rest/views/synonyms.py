# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SynonymSerializer


# Create your views here.
class SynonymViewSet(viewsets.ModelViewSet):
    queryset = db.Synonym.objects.all()
    serializer_class = SynonymSerializer
