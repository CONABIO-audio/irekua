# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import licence_types
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.LicenceType
        fields = (
            'name',
            'years_valid_for',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations'
        )


class LicenceTypeViewSet(BaseViewSet):
    queryset = db.LicenceType.objects.all()
    serializer_module = licence_types
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
