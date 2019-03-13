# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import EventTypeSerializer


class EventTypeViewSet(ModelViewSet):
    queryset = db.EventType.objects.all()
    serializer_class = EventTypeSerializer
    search_fields = ('name', )
    filter_fields = ('name', )
