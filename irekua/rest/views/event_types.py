# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

import database.models as db
from rest.serializers import EventTypeSerializer, TermTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


class EventTypeViewSet(ModelViewSet):
    queryset = db.EventType.objects.all()
    serializer_class = EventTypeSerializer

    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )

    @action(detail=True, methods=['GET'])
    def label_types(self, request, pk=None):
        try:
            event_type = db.EventType.objects.get(pk=pk)
        except db.EventType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        label_types = event_type.label_term_types.all()
        page = self.paginate_queryset(label_types)

        if page is not None:
            serializer = TermTypeSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = TermTypeSerializer(label_types, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], serializer_class=TermTypeSerializer)
    def add_label_type(self, request, pk=None):
        try:
            event_type = db.EventType.objects.get(pk=pk)
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = TermTypeSerializer(data=request.data)
        serializer.is_valid()
        if 'name' not in serializer.data:
            return Response('Invalid data. No term type name was provided', status=status.HTTP_400_BAD_REQUEST)

        try:
            term_type = db.TermType.objects.get(name=serializer.data['name'])
        except db.TermType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        event_type.label_term_types.add(term_type)
        event_type.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], serializer_class=TermTypeSerializer)
    def remove_label_type(self, request, pk=None):
        try:
            event_type = db.EventType.objects.get(pk=pk)
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = TermTypeSerializer(data=request.data)
        serializer.is_valid()
        if 'name' not in serializer.data:
            return Response('Invalid data. No term type name was provided', status=status.HTTP_400_BAD_REQUEST)

        try:
            term_type = event_type.label_term_types.get(name=serializer.data['name'])
        except db.TermType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        event_type.label_term_types.remove(term_type)
        event_type.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
