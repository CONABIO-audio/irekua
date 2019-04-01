# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import synonym_suggestions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import SynonymSuggestionFilter


class IsOwnSuggestion(BasePermission):
    def has_permission(self, request, view):
        try:
            suggestion = view.get_object()
            user = request.user
            return suggestion.suggested_by == user
        except (AttributeError, AssertionError):
            return False


class SynonymSuggestionViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.SynonymSuggestion.objects.all()
    serializer_mapping = SerializerMapping.from_module(synonym_suggestions)
    permission_classes = (IsAdmin | IsOwnSuggestion | ReadAndCreateOnly, )
    search_fields = ('source__value', 'synonym')
    filter_class = SynonymSuggestionFilter
