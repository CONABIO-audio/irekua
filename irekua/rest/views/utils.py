# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


class AdditionalActions(object):
    related_objects = []

    def return_related_object_list(self, request, queryset, serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_related_object(
            self,
            request,
            serializer_class,
            model_class,
            extra=None):

        serializer = serializer_class(
            data=request.data,
            context={'request': request})

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        extra_dict = {}
        if extra is not None:
            for extra_value in extra:
                extra_dict[extra_value] = (
                    serializer.validated_data.pop(extra_value))

        _, pk = serializer.validated_data.popitem()

        related_object = get_object_or_404(
            model_class,
            pk=pk)

        return related_object, extra_dict

    def filter_related_queryset(
            self,
            request,
            manager):
        queryset = manager.filter(**request.query_params)
        return queryset

    def add_related_object_view(
            self,
            request,
            model,
            method_name,
            extra=None):
        view_object = self.get_object()
        serializer = self.get_serializer_class()
        related_object, extra_dict = self.get_related_object(
            request,
            serializer,
            model,
            extra=extra)
        method = getattr(view_object, method_name)
        method(related_object, **extra_dict)
        return Response(status=status.HTTP_200_OK)
