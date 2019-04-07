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
from database.models import EventType
from database.models import AnnotationType

from rest.serializers.items import items
from rest.serializers.items import tags as tag_serializers
from rest.serializers.items import secondary_items as secondary_item_serializers
from rest.serializers.object_types import item_types
from rest.serializers.object_types import event_types as event_type_serializers
from rest.serializers.object_types import annotation_types as annotation_type_serializers
from rest.serializers.annotations import annotations as annotation_serializers

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import IsDeveloper
from rest.permissions import IsModel
from rest.permissions import IsSpecialUser
from rest.permissions import items as permissions

from rest.filters import ItemFilter

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class ItemViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  CustomViewSetMixin,
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
            tags=tag_serializers.ListSerializer,
            add_tag=tag_serializers.CreateSerializer,
            tag_item=tag_serializers.SelectSerializer,
            untag_item=tag_serializers.SelectSerializer,
            event_types=event_type_serializers.ListSerializer,
            add_event_type=event_type_serializers.CreateSerializer,
            annotation_types=annotation_type_serializers.ListSerializer,
            add_annotation_type=annotation_type_serializers.CreateSerializer,
            secondary_items=secondary_item_serializers.ListSerializer,
            add_secondary_item=secondary_item_serializers.CreateSerializer,
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
        'add_event_type': [IsAuthenticated, IsAdmin],
        'add_annotation_type': [IsAuthenticated, IsAdmin | IsDeveloper],
        'secondary_items': [
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
        'add_secondary_item': [
            IsAuthenticated,
            (
                permissions.IsCreator | # TODO: Add correct permissions
                IsSpecialUser
            )
        ]
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

    @action(detail=True, methods=['GET'])
    def secondary_items(self, request, pk=None):
        item = self.get_object()
        queryset = item.secondaryitem_set.all()
        return self.list_related_object_view(queryset)

    @secondary_items.mapping.post
    def add_secondary_item(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = ItemType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def event_types(self, request):
        queryset = EventType.objects.all()
        return self.list_related_object_view(queryset)

    @event_types.mapping.post
    def add_event_type(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def event_types(self, request):
        queryset = EventType.objects.all()
        return self.list_related_object_view(queryset)

    @event_types.mapping.post
    def add_event_type(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def annotation_types(self, request):
        queryset = AnnotationType.objects.all()
        return self.list_related_object_view(queryset)

    @annotation_types.mapping.post
    def add_annotation_type(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['POST'])
    def tag_item(self, request, pk=None):
        return self.add_related_object_view(Tag, 'tag')

    @action(detail=True, methods=['POST'])
    def untag_item(self, request, pk=None):
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
