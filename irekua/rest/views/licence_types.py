# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import LicenceType

from rest.serializers import licence_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.filters import LicenceTypeFilter


class LicenceTypeViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = LicenceType.objects.all()
    filterset_class = LicenceTypeFilter
    search_fields = ('name', )

    serializer_mapping = SerializerMapping.from_module(licence_types)
    permission_classes = (IsAdmin | ReadOnly, )
