# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from database.models import AnnotationVote

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest.serializers import annotation_votes
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping

from rest.permissions import PermissionMappingMixin
from rest.permissions import PermissionMapping
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import IsAuthenticated
from rest.permissions import annotation_votes as permissions

from rest.utils import Actions


class AnnotationVoteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            PermissionMappingMixin,
                            GenericViewSet):
    queryset = AnnotationVote.objects.all()

    serializer_mapping = SerializerMapping.from_module(annotation_votes)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
        Actions.RETRIEVE: [
            IsAuthenticated,
            (
                permissions.HasViewPermission |
                permissions.IsCreator |
                permissions.IsOpen |
                IsSpecialUser
            ),
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            permissions.IsCreator | IsAdmin,
        ],
    })
