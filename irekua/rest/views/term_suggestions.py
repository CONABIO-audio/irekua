# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import term_suggestions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import TermSuggestionFilter


class IsOwnSuggestion(BasePermission):
    def has_permission(self, request, view):
        try:
            suggestion = view.get_object()
            user = request.user
            return suggestion.suggested_by == user
        except:
            return False


class TermSuggestionViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.TermSuggestion.objects.all()
    serializer_mapping = SerializerMapping.from_module(term_suggestions)
    permission_classes = (IsAdmin | IsOwnSuggestion | ReadAndCreateOnly, )
    search_fields = ('term_type__name, value')
    filter_class = TermSuggestionFilter
