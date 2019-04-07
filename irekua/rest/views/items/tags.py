# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Tag

from rest.serializers.items import tags
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin

from rest.utils import Actions
from rest.filters import TagFilter


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 SerializerMappingMixin,
                 PermissionMappingMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_mapping = SerializerMapping.from_module(tags)
    search_fields = ('name', )
    filterset_class = TagFilter
    permission_classes = PermissionMapping({
        Actions.UPDATE: [IsAuthenticated, IsAdmin],
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)
