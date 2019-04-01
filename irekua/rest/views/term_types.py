# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import term_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly
from rest.filters import TermTypeFilter


class TermTypeViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.TermType.objects.all()
    serializer_mapping = SerializerMapping.from_module(term_types)
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = TermTypeFilter
