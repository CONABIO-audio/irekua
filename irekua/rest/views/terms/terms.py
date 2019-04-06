# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database.models import Term

from rest.serializers.terms import terms
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.filters import TermFilter
from rest.utils import Actions


class TermViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  SerializerMappingMixin,
                  PermissionMappingMixin,
                  GenericViewSet):
    queryset = Term.objects.all()
    search_fields = ('term_type__name', 'value',)
    filterset_class = TermFilter

    serializer_mapping = SerializerMapping.from_module(terms)

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [IsAuthenticated, IsAdmin | IsDeveloper],
        Actions.DESTROY: [IsAuthenticated, IsAdmin | IsDeveloper],
    }, default=IsAuthenticated)
