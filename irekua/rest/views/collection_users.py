# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import database.models as db
from rest.serializers import collection_users
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.User
        fields = (
            'username',
            'first_name',
            'last_name',
            'institution',
        )


class CollectionUserViewSet(BaseViewSet):
    queryset = db.CollectionUser.objects.all()
    serializer_module = collection_users
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'locality')
    filterset_class = Filter
