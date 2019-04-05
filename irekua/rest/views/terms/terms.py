# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database.models import Term

from rest.serializers.terms import terms
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin, IsDeveloper, ReadOnly

from rest.filters import TermFilter


class TermViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  SerializerMappingMixin,
                  GenericViewSet):
    queryset = Term.objects.all()
    serializer_mapping = SerializerMapping.from_module(terms)
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('term_type__name', 'value')
    filterset_class = TermFilter
