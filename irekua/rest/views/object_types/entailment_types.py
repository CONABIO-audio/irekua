# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import EntailmentType

from rest.serializers.object_types import entailment_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly

from rest.filters import EntailmentTypeFilter


class EntailmentTypeViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = EntailmentType.objects.all()
    serializer_mapping = SerializerMapping.from_module(entailment_types)
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('source_type__name', 'target_type__name')
    filterset_class = EntailmentTypeFilter
