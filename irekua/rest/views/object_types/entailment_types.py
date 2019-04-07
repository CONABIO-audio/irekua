# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import EntailmentType

from rest.serializers.object_types import entailment_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.utils import Actions
from rest.filters import EntailmentTypeFilter


class EntailmentTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):
    queryset = EntailmentType.objects.all()
    filterset_class = EntailmentTypeFilter
    search_fields = ('source_type__name', 'target_type__name')

    serializer_mapping = SerializerMapping.from_module(entailment_types)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [IsAuthenticated, IsDeveloper | IsAdmin],
        Actions.DESTROY: [IsAuthenticated, IsDeveloper | IsAdmin],
    }, default=IsAuthenticated)
