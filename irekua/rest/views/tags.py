# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import tags
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Tag
        fields = (
            'name',
        )


class TagViewSet(BaseViewSet):
    queryset = db.Tag.objects.all()
    serializer_module = tags
    search_fields = ('name', )
    filterset_class = Filter
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
