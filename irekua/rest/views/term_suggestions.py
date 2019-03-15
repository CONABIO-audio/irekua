# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import BasePermission
import django_filters

import database.models as db
from rest.serializers import TermSuggestionSerializer
from rest.permissions import IsAdmin, ReadAndCreateOnly


class SuggestionFilter(django_filters.FilterSet):
    suggested_on__gt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')
    suggested_on__lt = django_filters.DateTimeFilter(
        field_name='suggested_on',
        lookup_expr='gt')

    class Meta:
        model = db.TermSuggestion
        fields = (
            'term_type__name',
            'value',
            'suggested_by__username',
            'suggested_by__first_name',
            'suggested_by__is_superuser',
            'suggested_by__userdata__is_curator'
        )

class IsOwnSuggestion(BasePermission):
    def has_permission(self, request, view):
        try:
            suggestion = view.get_object()
            user = request.user
            return suggestion.suggested_by == user
        except:
            return False


class TermSuggestionViewSet(viewsets.ModelViewSet):
    queryset = db.TermSuggestion.objects.all()
    serializer_class = TermSuggestionSerializer
    permission_classes = (IsAdmin | IsOwnSuggestion | ReadAndCreateOnly, )
    search_fields = ('term_type__name, value')
    filter_class = SuggestionFilter
