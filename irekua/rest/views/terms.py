# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import terms
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Term
        fields = (
            'term_type__name',
            'value'
        )


class TermViewSet(BaseViewSet):
    queryset = db.Term.objects.all()
    serializer_module = terms
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('term_type__name', 'value')
    filterset_class = Filter
