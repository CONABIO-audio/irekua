# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from database import models as db

from rest.serializers import annotations
from rest.serializers import annotation_votes
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping
from rest.filters import AnnotationFilter
from rest.utils import Actions
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import annotations as annotation_permissions

from .utils import AdditionalActionsMixin


class AnnotationViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        SerializerMappingMixin,
                        PermissionMappingMixin,
                        GenericViewSet,
                        AdditionalActionsMixin):
    queryset = db.Annotation.objects.all()
    filterset_class = AnnotationFilter

    permission_mapping = PermissionMapping({
        Actions.UPDATE: annotation_permissions.CanUpdate,
        Actions.RETRIEVE: annotation_permissions.CanRetrieve,
        Actions.DESTROY: annotation_permissions.CanDestroy,
        Actions.LIST: annotation_permissions.CanList,
        'vote': annotation_permissions.CanVote,
        'votes': annotation_permissions.CanListVotes,
    })
    serializer_mapping = (
        SerializerMapping
        .from_module(annotations)
        .extend(
            vote=annotation_votes.CreateSerializer,
            votes=annotation_votes.ListSerializer
        ))

    def get_serializer_context(self):
        context = super().get_serializer_context()

        try:
            annotation = self.get_object()
        except AssertionError:
            annotation = None

        context['annotation'] = annotation
        return context

    @action(detail=True, methods=['GET'])
    def votes(self, request, pk=None):
        queryset = self.get_object().annotationvote_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['POST'])
    def vote(self, request, pk=None):
        return self.create_related_object_view()
