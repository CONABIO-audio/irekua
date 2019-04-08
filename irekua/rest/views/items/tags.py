# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Tag

from rest.serializers.items import tags

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 CustomViewSetMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()

    serializer_mapping = SerializerMapping.from_module(tags)
    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
