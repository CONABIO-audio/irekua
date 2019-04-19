# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import utils
from rest import serializers

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly


class TagViewSet(mixins.UpdateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.DestroyModelMixin,
                 utils.CustomViewSetMixin,
                 GenericViewSet):
    queryset = models.Tag.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.items.tags)

    permission_mapping = utils.PermissionMapping(default=IsAdmin | ReadOnly)