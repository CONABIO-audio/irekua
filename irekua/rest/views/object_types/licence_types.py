# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import LicenceType

from rest.serializers.object_types import licence_types

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class LicenceTypeViewSet(mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.UpdateModelMixin,
                         CustomViewSetMixin,
                         GenericViewSet):
    queryset = LicenceType.objects.all()

    serializer_mapping = SerializerMapping.from_module(licence_types)
    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated, IsAdmin],
        Actions.UPDATE: [IsAuthenticated, IsAdmin],
    }, default=IsAuthenticated)
