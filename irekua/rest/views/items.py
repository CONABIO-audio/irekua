# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.contrib.auth.models import Permission
from django.shortcuts import redirect
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
import django_filters

import database.models as db

from rest.serializers import items
from rest.serializers import annotations as annotation_serializers
from rest.serializers import tags
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping
from rest.filters import ItemFilter
from rest.filters import AnnotationFilter

from .utils import AdditionalActionsMixin


class ItemViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  SerializerMappingMixin,
                  AdditionalActionsMixin,
                  GenericViewSet):
    filterset_class = ItemFilter
    search_fields = ('item_type__name', )

    serializer_mapping = (
        SerializerMapping
        .from_module(items)
        .extend(
            annotations=annotation_serializers.ListSerializer,
            add_annotation=annotation_serializers.CreateSerializer,
            download=items.DownloadSerializer,
            upload=items.DownloadSerializer,
            add_tag=tags.SelectSerializer,
            remove_tag=tags.SelectSerializer
        ))

    def get_queryset(self):
        if self.action == 'annotations':
            item = self.kwargs['pk']
            return db.Annotation.objects.filter(item=item)

        user = self.request.user

        is_special_user = (
            user.is_superuser |
            user.is_curator |
            user.is_model |
            user.is_developer
        )
        if is_special_user:
            return self.get_full_queryset()

        return self.get_normal_queryset(user)

    def get_normal_queryset(self, user):
        is_open = (
            Q(licence__is_active=False) |
            Q(licence__licence_type__can_view=True)
        )
        is_owner = Q(sampling_event__created_by=user.pk)

        perm = Permission.objects.get(codename='view_collection_items')
        collections_with_permission = (
            db.CollectionUser.filter(
                user=user.pk,
                role__in=perm.role_set.all()
            ).select_related('collection')
        )

        is_in_allowed_collection = Q(
            sampling_event__collection__in=collections_with_permission)

        filter_query = (
            is_open |
            is_owner |
            is_in_allowed_collection
        )

        queryset = db.Item.objects.filter(filter_query)
        return queryset

    def get_full_queryset(self):
        return db.Item.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            item = self.get_object()
        except AssertionError:
            item = None

        context['item'] = item
        return context

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=AnnotationFilter)
    def annotations(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def add_annotation(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=True, methods=['POST'])
    def add_tag(self, request, pk=None):
        return self.add_related_object_view(db.Tag, 'tag')

    @action(detail=True, methods=['POST'])
    def remove_tag(self, request, pk=None):
        return self.remove_related_object_view('tag')

    @action(detail=True, methods=['POST'])
    def upload(self, request, pk=None):
        item = self.get_object()

        if item.item_file.name != '':
            return Response(
                'File previously uploaded',
                status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(item, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response('Invalid file', status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response('File uploaded', status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        item = self.get_object()

        if item.item_file.name == '':
            return Response(
                'File not uploaded to server',
                status=status.HTTP_404_NOT_FOUND)

        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        serializer = serializer_class(item, context=context)

        url = serializer.data['item_file']
        return redirect(url)
