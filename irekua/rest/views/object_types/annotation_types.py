# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import AnnotationType

from rest.serializers.object_types import annotation_types

from rest.permissions import IsDeveloper
from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class AnnotationTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):
    queryset = AnnotationType.objects.all()

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            IsDeveloper | IsAdmin,
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin,
        ],
    }, default=IsAuthenticated)
    serializer_mapping = SerializerMapping.from_module(annotation_types)
