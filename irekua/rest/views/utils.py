# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
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
            pk_field='pk',
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

        query = {
            pk_field: pk
        }
        related_object = get_object_or_404(
            model_class,
            **query)

        return related_object, extra_dict

    def create_related_object(
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

        related_object = model_class.objects.create(
            **serializer.validated_data)

        return related_object, extra_dict

    def add_related_object_view(
            self,
            model,
            name,
            pk_field='pk',
            extra=None):
        request = self.request
        view_object = self.get_object()
        serializer = self.get_serializer_class()
        related_object, extra_dict = self.get_related_object(
            request,
            serializer,
            model,
            extra=extra,
            pk_field=pk_field)
        method_name = 'add_{name}'.format(name=name)
        method = getattr(view_object, method_name)
        method(related_object, **extra_dict)
        return Response(status=status.HTTP_200_OK)

    def remove_related_object_view(
            self,
            name,
            pk_field='pk',
            many=True):
        request = self.request
        view_object = self.get_object()
        serializer = self.get_serializer_class()

        suffix = 's' if many else '_set'
        related_manager_name = '{name}{suffix}'.format(
            name=name,
            suffix=suffix)
        related_objects = getattr(view_object, related_manager_name).all()
        related_object, _ = self.get_related_object(
            request,
            serializer,
            related_objects,
            pk_field=pk_field)

        method_name = 'remove_{name}'.format(name=name)
        method = getattr(view_object, method_name)
        method(related_object)
        return Response(status=status.HTTP_200_OK)

    def create_related_object_view(
            self,
            model,
            name,
            prefix='add',
            extra=None):
        request = self.request
        view_object = self.get_object()
        serializer = self.get_serializer_class()

        related_object, extra_dict = self.create_related_object(
            request,
            serializer,
            model,
            extra=extra)

        method_name = '{prefix}_{name}'.format(
            prefix=prefix,
            name=name)
        method = getattr(view_object, method_name)
        method(related_object, **extra_dict)
        return Response(status=status.HTTP_201_CREATED)
