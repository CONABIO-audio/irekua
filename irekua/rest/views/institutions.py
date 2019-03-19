# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import institutions
from rest.permissions import IsAdmin, IsFromInstitution, ReadAndCreateOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country'
        )


class InstitutionViewSet(BaseViewSet):
    queryset = db.Institution.objects.all()
    serializer_module = institutions
    search_fields = (
        'institution_name',
        'institution_code',
        'subdependency')
    filterset_class = Filter

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsFromInstitution]
        else:
            permission_classes = [IsAdmin | ReadAndCreateOnly]
        return [permission() for permission in permission_classes]
