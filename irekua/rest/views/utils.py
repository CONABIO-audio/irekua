# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response


_CREATE_ACTIONS = [
    'create',
    'update',
    'partial_update',
    'options'
]


class CustomViewSet(viewsets.GenericViewSet):
    @property
    def serializer_module(self):
        raise NotImplementedError

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_module.ListSerializer
        if self.action == 'retrieve':
            return self.serializer_module.DetailSerializer
        if self.action in _CREATE_ACTIONS:
            return self.serializer_module.CreateSerializer
        return super().get_serializer_class()


class NoCreateViewSet(mixins.ListModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      CustomViewSet):
    pass


class BaseViewSet(mixins.CreateModelMixin, NoCreateViewSet):
    pass


class AdditionalActions(object):
    def return_related_object_list(
            self,
            request,
            queryset,
            serializer_class):
        page = self.paginate_queryset(queryset)
        if page is not None:
            context = self.get_serializer_context()
            serializer = serializer_class(
                page,
                many=True,
                context=context)
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

        context = self.get_serializer_context()
        serializer = serializer_class(
            data=request.data,
            context=context)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        extra_dict = {}
        if extra is not None:
            for extra_value in extra:
                extra_dict[extra_value] = (
                    serializer.validated_data.pop(extra_value))

        _, pk = serializer.validated_data.popitem()

        if isinstance(pk, Model):
            return pk, extra_dict

        query = {pk_field: pk}
        related_object = get_object_or_404(
            model_class,
            **query)

        return related_object, extra_dict

    def create_related_object(
            self,
            request,
            serializer_class,
            extra=None):

        context = self.get_serializer_context()
        serializer = serializer_class(
            data=request.data,
            context=context)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        extra_dict = {}
        if extra is not None:
            for extra_value in extra:
                extra_dict[extra_value] = (
                    serializer.validated_data.pop(extra_value))

        related_object = serializer.save()
        return serializer, related_object, extra_dict

    def list_related_object_view(
            self,
            queryset):
        request = self.request
        serializer = self.get_serializer_class()
        return self.return_related_object_list(
            request,
            queryset,
            serializer)

    def add_related_object_view(
            self,
            model,
            name,
            pk_field='pk',
            extra=None,
            through_model=False):
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
            extra=None):
        request = self.request
        serializer_class = self.get_serializer_class()

        serializer, _, _ = self.create_related_object(
            request,
            serializer_class,
            extra=extra)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
