# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

import database.models as db
from rest.serializers import EntailmentSerializer
from rest.permissions import IsAdmin, IsCurator, ReadOnly


class EntailmentViewSet(viewsets.ModelViewSet):
    queryset = db.Entailment.objects.all()
    serializer_class = EntailmentSerializer
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
    search_fields = ('source__value', 'target__value')
    filter_fields = (
        'source__value',
        'source__term_type__name',
        'target__value',
        'target__term_type__name',
    )
