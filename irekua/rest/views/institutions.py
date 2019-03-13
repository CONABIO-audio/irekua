# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

import database.models as db
from rest.serializers import InstitutionSerializer
from rest.permissions import IsAdmin, IsFromInstitution, ReadOnly


# Create your views here.
class InstitutionViewSet(ModelViewSet):
    queryset = db.Institution.objects.all()
    serializer_class = InstitutionSerializer
    # permission_classes = (IsAdmin|ReadOnly|IsFromInstitution)
    search_fields = (
        'institution_name',
        'institution_code',
        'subdependency')
    filter_fields = (
        'institution_name',
        'institution_code',
        'subdependency',
        'country')

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            permission_classes = [IsFromInstitution]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
