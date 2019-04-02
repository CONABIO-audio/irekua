# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

import database.models as db

from rest.serializers import term_types
from rest.serializers import terms as term_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsDeveloper, ReadOnly
from rest.filters import TermTypeFilter
from .utils import AdditionalActionsMixin


class TermTypeViewSet(SerializerMappingMixin,
                      AdditionalActionsMixin,
                      ModelViewSet):
    queryset = db.TermType.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = TermTypeFilter
    serializer_mapping = (
        SerializerMapping
        .from_module(term_types)
        .extend(
            add_term=term_serializers.CreateSerializer,
            terms=term_serializers.ListSerializer
        ))

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            term_type = self.get_object()
        except (AssertionError, AttributeError):
            term_type = None

        context['term_type'] = term_type
        return context

    @action(detail=True, methods=['POST'])
    def add_term(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def terms(self, request, pk=None):
        term_type = self.get_object()
        queryset = term_type.term_set.all()
        return self.list_related_object_view(queryset)
