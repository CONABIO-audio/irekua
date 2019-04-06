# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database.models import Annotation
from database.models import AnnotationType

from rest.serializers.object_types import annotation_types
from rest.serializers.annotations import annotations
from rest.serializers.annotations import annotation_votes
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.filters import AnnotationFilter
from rest.utils import Actions

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import IsSpecialUser
from rest.permissions import annotations as permissions

from rest.views.utils import AdditionalActionsMixin


class AnnotationViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        SerializerMappingMixin,
                        PermissionMappingMixin,
                        GenericViewSet,
                        AdditionalActionsMixin):
    queryset = Annotation.objects.all()
    filterset_class = AnnotationFilter

    serializer_mapping = (
        SerializerMapping
        .from_module(annotations)
        .extend(
            vote=annotation_votes.CreateSerializer,
            votes=annotation_votes.ListSerializer,
            types=annotation_types.ListSerializer,
            add_type=annotation_types.CreateSerializer,
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
        Actions.LIST: IsAuthenticated,
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
        'types': IsAuthenticated,
        'add_type': [IsAuthenticated, IsAdmin],
    })

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            annotation = self.get_object()
        except (AssertionError, AttributeError):
            annotation = None

        context['annotation'] = annotation
        return context

    @action(detail=True, methods=['GET'])
    def votes(self, request, pk=None):
        queryset = self.get_object().annotationvote_set.all()
        return self.list_related_object_view(queryset)

    @votes.mapping.post
    def vote(self, request, pk=None):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = AnnotationType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        return self.create_related_object_view()
