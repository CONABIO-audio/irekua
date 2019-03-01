# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import EntailmentSerializer


# Create your views here.
class EntailmentViewSet(viewsets.ModelViewSet):
    queryset = db.Entailment.objects.all()
    serializer_class = EntailmentSerializer
