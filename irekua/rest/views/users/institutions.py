# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Institution

from rest.serializers.users import institutions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import institutions as permissions

from rest.filters import InstitutionFilter
from rest.utils import Actions


class InstitutionViewSet(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         SerializerMappingMixin,
                         PermissionMappingMixin,
                         GenericViewSet):
    queryset = Institution.objects.all()
    filterset_class = InstitutionFilter
    search_fields = (
        'institution_name',
        'institution_code',
        'subdependency')

    serializer_mapping = SerializerMapping.from_module(institutions)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsFromInstitution |
                IsAdmin
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin
        ],
    }, default=IsAuthenticated)
