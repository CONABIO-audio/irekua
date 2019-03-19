# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import action

import database.models as db
from rest.serializers import metacollections
from rest.serializers import items
from rest.permissions import IsAdmin, IsDeveloper, IsModel, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet, AdditionalActions


class Filter(BaseFilter):
    class Meta:
        model = db.MetaCollection
        fields = (
            'name',
        )


class MetaCollectionViewSet(BaseViewSet, AdditionalActions):
    queryset = db.MetaCollection.objects.all()
    serializer_module = metacollections
    permission_classes = (IsAdmin | IsDeveloper | IsModel | ReadOnly, )
    filterset_class = Filter
    search_fields = ('name', )

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=items.SelectSerializer)
    def add_item(self, request, pk=None):
        return self.add_related_object_view(
            db.Item,
            'item')

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=items.SelectSerializer)
    def remove_item(self, request, pk=None):
        return self.remove_related_object_view(
            'item')
