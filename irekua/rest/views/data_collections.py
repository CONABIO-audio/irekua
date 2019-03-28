# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

import database.models as db
from rest.serializers import data_collections
from rest.serializers import licences
from rest.serializers import devices
from rest.permissions import IsDeveloper, IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = db.Collection
        fields = (
            'name',
            'collection_type__name',
            'institution__institution_code',
            'institution__institution_name',
            'institution__country',
        )


class CollectionViewSet(BaseViewSet):
    queryset = db.Collection.objects.all()
    permission_classes = (IsAdmin | IsDeveloper | ReadOnly, )
    search_fields = ('name', )
    filterset_class = Filter
    serializer_module = data_collections

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            collection = self.get_object()
            context['collection'] = collection
        except:
            pass
        return context

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=licences.CreateSerializer)
    def create_licence(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        collection = self.get_object()

        serializer = serializer_class(
            data=request.data,
            context={
                'collection': collection,
                'request': request,
            })

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
