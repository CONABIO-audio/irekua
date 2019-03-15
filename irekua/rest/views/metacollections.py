# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import MetaCollectionSerializer
from rest.permissions import IsAdmin, IsDeveloper, IsModel, ReadOnly


class MetaCollectionViewSet(viewsets.ModelViewSet):
    queryset = db.MetaCollection.objects.all()
    serializer_class = MetaCollectionSerializer
    permission_classes = (IsAdmin | IsDeveloper | IsModel | ReadOnly, )
    search_fields = ('name', )
    filter_fields = (
        'name',
        'creator__username',
        'creator__first_name')
