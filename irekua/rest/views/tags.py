# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import TagSerializer


# Create your views here.
class TagViewSet(viewsets.ModelViewSet):
    queryset = db.Tag.objects.all()
    serializer_class = TagSerializer
