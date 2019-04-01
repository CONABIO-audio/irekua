# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import terms
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly
from rest.filters import TermFilter


class TermViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Term.objects.all()
    serializer_mapping = SerializerMapping.from_module(terms)
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('term_type__name', 'value')
    filterset_class = TermFilter
