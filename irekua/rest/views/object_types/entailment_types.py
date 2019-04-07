# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import EntailmentType

from rest.serializers.object_types import entailment_types

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class EntailmentTypeViewSet(mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.UpdateModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):
    queryset = EntailmentType.objects.all()

    serializer_mapping = SerializerMapping.from_module(entailment_types)
    permission_mapping = PermissionMapping(
        default=IsDeveloper | IsAdmin | ReadOnly)
