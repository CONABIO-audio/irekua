
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionSiteSerializer


# Create your views here.
class CollectionSiteViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionSite.objects.all()
    serializer_class = CollectionSiteSerializer
