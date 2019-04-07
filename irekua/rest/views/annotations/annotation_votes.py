# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import AnnotationVote

from rest.serializers.annotations import annotation_votes

from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
from rest.permissions import IsAuthenticated
from rest.permissions import annotation_votes as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class AnnotationVoteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSetMixin,
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
