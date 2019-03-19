# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import entailment_types
from rest.permissions import IsAdmin, ReadOnly, IsDeveloper
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.EntailmentType
        fields = (
            'source_type__name',
            'target_type__name',
        )


class EntailmentTypeViewSet(BaseViewSet):
    queryset = db.EntailmentType.objects.all()
    serializer_module = entailment_types
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('source_type__name', 'target_type__name')
    filterset_class = Filter
