# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import LicenceTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


# Create your views here.
class LicenceTypeViewSet(viewsets.ModelViewSet):
    queryset = db.LicenceType.objects.all()
    serializer_class = LicenceTypeSerializer
    permission_classes = (IsAdmin|ReadOnly, )
    search_fields = ('name', )
    filter_fields = (
        'name',
        'years_valid_for',
        'can_view',
        'can_download',
        'can_view_annotations',
        'can_annotate',
        'can_vote_annotations')
