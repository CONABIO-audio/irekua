# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import entailments
from rest.permissions import IsAdmin, IsCurator, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Entailment
        fields = (
            'source__value',
            'source__term_type__name',
            'target__value',
            'target__term_type__name',
        )


class EntailmentViewSet(BaseViewSet):
    queryset = db.Entailment.objects.all()
    serializer_module = entailments
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
    search_fields = ('source__value', 'target__value')
    filterset_class = Filter
