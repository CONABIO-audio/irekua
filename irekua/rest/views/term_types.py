# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import term_types
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.TermType
        fields = ('name', )


class TermTypeViewSet(BaseViewSet):
    queryset = db.TermType.objects.all()
    serializer_module = term_types
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
