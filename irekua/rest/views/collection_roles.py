
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import CollectionRoleSerializer


# Create your views here.
class CollectionRoleViewSet(viewsets.ModelViewSet):
    queryset = db.CollectionRole.objects.all()
    serializer_class = CollectionRoleSerializer
