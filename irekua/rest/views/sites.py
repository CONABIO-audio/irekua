# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SiteSerializer


# Create your views here.
class SiteViewSet(viewsets.ModelViewSet):
    queryset = db.Site.objects.all()
    serializer_class = SiteSerializer
