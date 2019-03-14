# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import SynonymSerializer
from rest.permissions import IsAdmin, IsCurator, ReadOnly


class SynonymViewSet(viewsets.ModelViewSet):
    queryset = db.Synonym.objects.all()
    serializer_class = SynonymSerializer
    search_fields = ('source__value', 'target__value')
    filter_fields = (
        'source__term_type__name',
        'source__value',
        'target__term_type__name',
        'target__value')
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
