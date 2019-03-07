# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import RoleSerializer


# Create your views here.
class RoleViewSet(viewsets.ModelViewSet):
    queryset = db.Role.objects.all()
    serializer_class = RoleSerializer
