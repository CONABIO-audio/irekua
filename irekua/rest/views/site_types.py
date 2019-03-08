# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SiteTypeSerializer


# Create your views here.
class SiteTypeViewSet(viewsets.ModelViewSet):
    queryset = db.SiteType.objects.all()
    serializer_class = SiteTypeSerializer
