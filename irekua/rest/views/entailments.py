# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import entailments
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsCurator, ReadOnly
from rest.filters import EntailmentFilter


class EntailmentViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Entailment.objects.all()
    serializer_mapping = SerializerMapping.from_module(entailments)
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
    search_fields = ('source__value', 'target__value')
    filterset_class = EntailmentFilter
