# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsDeveloper
from rest.permissions import IsAdmin
from rest.permissions import ReadOnly


class AnnotationToolViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            utils.CustomViewSetMixin,
                            GenericViewSet):
    queryset = models.AnnotationTool.objects.all()  # pylint: disable=E1101

    permission_mapping = utils.PermissionMapping(
        default=IsAdmin | IsDeveloper | ReadOnly)
    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.annotations.tools)
