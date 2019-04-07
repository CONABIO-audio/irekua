# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import Annotation
from database.models import AnnotationVote
from database.models import AnnotationType
from database.models import AnnotationTool

from rest.serializers.object_types import annotation_types
from rest.serializers.annotations import annotations
from rest.serializers.annotations import annotation_votes
from rest.serializers.annotations import annotation_tools as annotation_tool_serializers

from rest import filters

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import IsSpecialUser
from rest.permissions import annotations as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class AnnotationViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        CustomViewSetMixin,
                        GenericViewSet):
    queryset = Annotation.objects.all()
    filterset_class = filters.annotations.Filter
    search_fields = filters.annotations.search_fields

    serializer_mapping = (
        SerializerMapping
        .from_module(annotations)
        .extend(
            vote=annotation_votes.CreateSerializer,
            votes=annotation_votes.ListSerializer,
            types=annotation_types.ListSerializer,
            add_type=annotation_types.CreateSerializer,
            tools=annotation_tool_serializers.ListSerializer,
            add_tool=annotation_tool_serializers.CreateSerializer,
        ))

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasUpdatePermission |
                IsCurator |
                IsAdmin
            ),
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
        'vote': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasVotePermission |
                IsCurator |
                IsAdmin
            ),
        ],
        'votes': [
            IsAuthenticated,
            (
                permissions.IsCreator |
                permissions.HasViewPermission |
                permissions.IsCollectionAdmin |
                permissions.IsCollectionTypeAdmin |
                IsSpecialUser
            ),
        ],
        'add_type': [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            annotation = self.get_object()
        except (AssertionError, AttributeError):
            annotation = None

        context['annotation'] = annotation
        return context

    def get_queryset(self):
        if self.action == 'votes':
            annotation_id = self.kwargs['pk']
            return AnnotationVote.objects.filter(annotation=annotation_id)

        if self.action == 'types':
            return AnnotationType.objects.all()

        if self.action == 'tools':
            return AnnotationTool.objects.all()

        return super().get_queryset()

    @action(
        detail=True,
        methods=['GET'],
        filterset_class=filters.annotation_votes.Filter,
        search_fields=filters.annotation_votes.search_fields)
    def votes(self, request, pk=None):
        return self.list_related_object_view()

    @votes.mapping.post
    def vote(self, request, pk=None):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.annotation_types.Filter,
        search_fields=filters.annotation_types.search_fields)
    def types(self, request):
        return self.list_related_object_view()

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()

    @action(
        detail=False,
        methods=['GET'],
        filterset_class=filters.annotation_tools.Filter,
        search_fields=filters.annotation_tools.search_fields)
    def tools(self, request):
        return self.list_related_object_view()

    @tools.mapping.post
    def add_tool(self, request):
        return self.create_related_object_view()
