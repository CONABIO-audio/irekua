# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import TermSerializer
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly


class TermViewSet(ModelViewSet):
    queryset = db.Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = (IsAdmin|IsDeveloper|ReadOnly, )
    search_fields = ('term_type__name', 'value')
    filter_fields = ('term_type__name', 'value')
