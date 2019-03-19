# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
import django_filters

import database.models as db
from rest.serializers import synonym_suggestions
from rest.permissions import IsAdmin, ReadAndCreateOnly
from .utils import BaseViewSet


class SuggestionFilter(django_filters.FilterSet):
    suggested_on__gt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')
    suggested_on__lt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')

    class Meta:
        model = db.SynonymSuggestion
        fields = (
            'source__term_type__name',
            'source__value',
            'synonym',
            'suggested_by__username',
            'suggested_by__first_name',
        )


class IsOwnSuggestion(BasePermission):
    def has_permission(self, request, view):
        try:
            suggestion = view.get_object()
            user = request.user
            return suggestion.suggested_by == user
        except:
            return False


class SynonymSuggestionViewSet(BaseViewSet):
    queryset = db.SynonymSuggestion.objects.all()
    serializer_module = synonym_suggestions
    permission_classes = (IsAdmin | IsOwnSuggestion | ReadAndCreateOnly, )
    search_fields = ('source__value', 'synonym')
    filter_class = SuggestionFilter
