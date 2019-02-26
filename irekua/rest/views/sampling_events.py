# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SamplingEventSerializer


# Create your views here.
class SamplingEventViewSet(viewsets.ModelViewSet):
    queryset = db.SamplingEvent.objects.all()
    serializer_class = SamplingEventSerializer
