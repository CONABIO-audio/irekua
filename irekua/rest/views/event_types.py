# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import EventTypeSerializer


# Create your views here.
class EventTypeViewSet(viewsets.ModelViewSet):
    queryset = db.EventType.objects.all()
    serializer_class = EventTypeSerializer
