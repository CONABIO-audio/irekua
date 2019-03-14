# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import TagSerializer
from rest.permissions import IsAdmin, ReadAndCreateOnly


class TagViewSet(viewsets.ModelViewSet):
    queryset = db.Tag.objects.all()
    serializer_class = TagSerializer
    search_fields = ('name', )
    filter_fields = ('name', )
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
