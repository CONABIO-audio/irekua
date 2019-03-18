# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import sampling_events


class SamplingEventViewSet(viewsets.ModelViewSet):
    queryset = db.SamplingEvent.objects.all()
    serializer_class = sampling_events.CreateSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return sampling_events.ListSerializer
        if self.action == 'retrieve':
            return sampling_events.DetailSerializer

        return super().get_serializer_class()
