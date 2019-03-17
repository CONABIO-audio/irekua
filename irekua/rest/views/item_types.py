# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

import database.models as db
from rest.serializers import ItemTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = db.EventType
        fields = (
            'url',
            'name'
        )


class ItemTypeViewSet(viewsets.ModelViewSet):
    queryset = db.ItemType.objects.all()
    serializer_class = ItemTypeSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'media_type', )
    filter_fields = (
        'name',
        'media_type'
    )

    @action(detail=True, methods=['GET'])
    def event_types(self, request, pk=None):
        try:
            item_type = db.ItemType.objects.get(pk=pk)
        except db.ItemType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        event_types = item_type.event_types.all()
        page = self.paginate_queryset(event_types)

        if page is not None:
            serializer = EventTypeSerializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = EventTypeSerializer(
            event_types,
            many=True)
        return Response(serializer.data)

    @action(
            detail=True,
            methods=['POST'],
            serializer_class=EventTypeSerializer)
    def add_event_type(self, request, pk=None):
        try:
            item_type = db.ItemType.objects.get(pk=pk)
        except db.ItemType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = EventTypeSerializer(data=request.data)
        serializer.is_valid()
        if 'name' not in serializer.data:
            return Response(
                'Invalid data. No event type was provided',
                status=status.HTTP_400_BAD_REQUEST)

        try:
            event_type = db.EventType.objects.get(name=serializer.data['name'])
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        item_type.event_types.add(event_type)
        item_type.save()
        return Response(status=status.HTTP_200_OK)

    @action(
            detail=True,
            methods=['POST'],
            serializer_class=EventTypeSerializer)
    def remove_event_type(self, request, pk=None):
        try:
            item_type = db.ItemType.objects.get(pk=pk)
        except db.ItemType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = EventTypeSerializer(data=request.data)
        serializer.is_valid()
        if 'name' not in serializer.data:
            return Response(
                'Invalid data. No event type was provided',
                status=status.HTTP_400_BAD_REQUEST)

        try:
            event_type = item_type.event_types.get(
                name=serializer.data['name'])
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        item_type.event_types.remove(event_type)
        item_type.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
