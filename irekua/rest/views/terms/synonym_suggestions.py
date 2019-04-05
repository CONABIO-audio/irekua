# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission
from rest_framework.viewsets import ModelViewSet

from database.models import SynonymSuggestion

from rest.serializers.terms import synonym_suggestions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
import rest.permissions.synonym_suggestions as permissions

from rest.utils import Actions
from rest.filters import SynonymSuggestionFilter



class SynonymSuggestionViewSet(SerializerMappingMixin,
                               PermissionMappingMixin,
                               ModelViewSet):
    queryset = SynonymSuggestion.objects.all()
    search_fields = ('source__value', 'synonym')
    filter_class = SynonymSuggestionFilter
    serializer_mapping = SerializerMapping.from_module(synonym_suggestions)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
        ],
        Actions.DESTROY: [
            IsAuthenticated,
        ]
    }, default=IsAuthenticated)
