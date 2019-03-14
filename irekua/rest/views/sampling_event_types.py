# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import SamplingEventTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


class SamplingEventTypeViewSet(viewsets.ModelViewSet):
    queryset = db.SamplingEventType.objects.all()
    serializer_class = SamplingEventTypeSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filter_fields = (
        'name',
        'restrict_device_types',
        'restrict_site_types')
