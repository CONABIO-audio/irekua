
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionUserSerializer


# Create your views here.
class CollectionUserViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionUser.objects.all()
    serializer_class = CollectionUserSerializer
