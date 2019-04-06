# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import TermSuggestion

from rest.serializers.terms import term_suggestions
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


class TermSuggestionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            GenericViewSet):
    queryset = TermSuggestion.objects.all()
    serializer_mapping = SerializerMapping.from_module(term_suggestions)
    permission_classes = (IsAdmin | IsOwnSuggestion | ReadAndCreateOnly, )
    search_fields = ('term_type__name, value')
    filter_class = TermSuggestionFilter
