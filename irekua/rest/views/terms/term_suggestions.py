# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import TermSuggestion

from rest.serializers.terms import term_suggestions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import term_suggestions as permissions
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.utils import Actions
from rest.filters import TermSuggestionFilter


class TermSuggestionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            PermissionMappingMixin,
                            SerializerMappingMixin,
                            GenericViewSet):
    queryset = TermSuggestion.objects.all()
    search_fields = ('term_type__name, value')
    filter_class = TermSuggestionFilter
    serializer_mapping = SerializerMapping.from_module(term_suggestions)

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsOwnSuggestion | IsAdmin
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsOwnSuggestion | IsAdmin
        ],
    }, default=IsAuthenticated)
