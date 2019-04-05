# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import Synonym

from rest.serializers.terms import synonyms
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin, IsCurator, ReadOnly

from rest.filters import SynonymFilter


class SynonymViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = Synonym.objects.all()
    serializer_mapping = SerializerMapping.from_module(synonyms)
    search_fields = ('source__value', 'target__value')
    filterset_class = SynonymFilter
    permission_classes = (IsAdmin | IsCurator | ReadOnly, )
