# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SamplingEventTypeSerializer


# Create your views here.
class SamplingEventTypeViewSet(viewsets.ModelViewSet):
    queryset = db.SamplingEventType.objects.all()
    serializer_class = SamplingEventTypeSerializer
