# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db
from rest.serializers import institutions
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, IsFromInstitution, ReadAndCreateOnly
from rest.filters import InstitutionFilter


class InstitutionViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Institution.objects.all()
    serializer_mapping = SerializerMapping.from_module(institutions)
    search_fields = (
        'institution_name',
        'institution_code',
        'subdependency')
    filterset_class = InstitutionFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsFromInstitution]
        else:
            permission_classes = [IsAdmin | ReadAndCreateOnly]
        return [permission() for permission in permission_classes]
