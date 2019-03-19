# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import synonyms
from rest.permissions import IsAdmin, IsCurator, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Synonym
        fields = (
            'source__term_type__name',
            'source__value',
            'target__term_type__name',
            'target__value'
        )


class SynonymViewSet(BaseViewSet):
    queryset = db.Synonym.objects.all()
    serializer_module = synonyms
    search_fields = ('source__value', 'target__value')
    filterset_class = Filter
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
