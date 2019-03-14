# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import DeviceTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


class DeviceTypeViewSet(ModelViewSet):
    queryset = db.DeviceType.objects.all()
    serializer_class = DeviceTypeSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )
