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

from database.models import CollectionUser
from database.models import Tag
from database.models import Annotation
from database.models import Item
from database.models import ItemType

from rest.serializers.items import items
from rest.serializers.items import tags
from rest.serializers.object_types import item_types
from rest.serializers.annotations import annotations as annotation_serializers
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import IsModel
from rest.permissions import IsSpecialUser
from rest.permissions import items as permissions

from rest.filters import ItemFilter
from rest.utils import Actions

from rest.views.utils import AdditionalActionsMixin


class ItemViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  SerializerMappingMixin,
                  PermissionMappingMixin,
                  AdditionalActionsMixin,
                  GenericViewSet):
    queryset = Item.objects.all()
    filterset_class = ItemFilter
    search_fields = ('item_type__name', )

    serializer_mapping = (
        SerializerMapping
        .from_module(items)
        .extend(
            annotations=annotation_serializers.ListSerializer,
            add_annotation=annotation_serializers.CreateSerializer,
            types=item_types.ListSerializer,
            add_type=item_types.CreateSerializer,
            download=items.DownloadSerializer,
            upload=items.DownloadSerializer,
            add_tag=tags.SelectSerializer,
            remove_tag=tags.SelectSerializer
        ))
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasUpdatePermission |
                IsAdmin
            )
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToView |
                IsSpecialUser
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        'annotations': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewAnnotationsPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToViewAnnotations |
                IsSpecialUser
            )
        ],
        'add_annotation': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasAddAnnotationPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToAnnotate |
                IsCurator |
                IsModel |
                IsAdmin
            )
        ],
        'tag_item': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsCurator |
                IsAdmin
            )
        ],
        'remove_tag': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsCurator |
                IsAdmin
            )
        ],
        'upload': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        'download': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasDownloadPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                permissions.ItemIsOpenToDownload |
                IsSpecialUser
            )
        ],
        'add_type': [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            item = self.get_object()
        except (AssertionError, AttributeError):
            item = None

        context['item'] = item
        return context

    @action(detail=False, methods=['GET'])
    def tags(self, request):
        queryset = Tag.objects.all()
        return self.list_related_object_view(queryset)

    @tags.mapping.post
    def add_tag(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'])
    def annotations(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @annotations.mapping.post
    def add_annotation(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = ItemType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['POST'])
    def tag_item(self, request, pk=None):
        return self.add_related_object_view(Tag, 'tag')

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

    def get_queryset(self):
        if self.action in Actions.DEFAULT_ACTIONS:
            return self.get_queryset_for_default_actions()

        return self.get_queryset_for_additional_actions()

    def get_queryset_for_additional_actions(self):
        if self.action == 'annotations':
            item_pk = self.kwargs['pk']
            queryset = Annotation.objects.filter(item=item_pk)
            return queryset

        return Item.objects.all()

    def get_queryset_for_default_actions(self):
        try:
            user = self.request.user
        except AttributeError:
            return Item.objects.none()

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
            CollectionUser.objects
            .filter(
                user=user.pk,
                role__in=perm.role_set.all()
            ).values('collection')
        )
        # TODO
        # Check that this query is working

        is_in_allowed_collection = Q(
            sampling_event__collection__in=collections_with_permission)

        filter_query = (
            is_open |
            is_owner |
            is_in_allowed_collection
        )

        queryset = Item.objects.filter(filter_query)
        return queryset

    def get_full_queryset(self):
        return Item.objects.all()
