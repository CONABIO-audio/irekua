# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import RoleTypeSerializer


# Create your views here.
class RoleTypeViewSet(viewsets.ModelViewSet):
    queryset = db.RoleType.objects.all()
    serializer_class = RoleTypeSerializer
