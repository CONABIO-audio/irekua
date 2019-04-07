# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import AnnotationTool

from rest.serializers.annotations import annotation_tools

from rest.permissions import IsDeveloper
from rest.permissions import IsAdmin
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class AnnotationToolViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):
    queryset = AnnotationTool.objects.all()

    permission_mapping = PermissionMapping(
        default=IsAdmin | IsDeveloper | ReadOnly)
    serializer_mapping = SerializerMapping.from_module(annotation_tools)
