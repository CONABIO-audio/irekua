# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SiteType

from rest.serializers.object_types import site_types

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class SiteTypeViewSet(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      CustomViewSetMixin,
                      GenericViewSet):
    queryset = SiteType.objects.all()

    serializer_mapping = SerializerMapping.from_module(site_types)
    permission_mapping = PermissionMapping({
        Actions.DESTROY: [IsAuthenticated | IsAdmin],
        Actions.UPDATE: [IsAuthenticated | IsAdmin],
    }, default=IsAuthenticated)
