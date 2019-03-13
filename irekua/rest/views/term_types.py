# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import TermTypeSerializer
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly


class TermTypeViewSet(ModelViewSet):
    queryset = db.TermType.objects.all()
    serializer_class = TermTypeSerializer
    permission_classes = (IsAdmin|IsDeveloper|ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )
