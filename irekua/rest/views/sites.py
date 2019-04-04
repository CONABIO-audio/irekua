# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import Site

from rest.serializers import sites
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import IsSpecialUser
import rest.permissions.sites as permissions

from rest.filters import SiteFilter
from rest.utils import Actions


class SiteViewSet(SerializerMappingMixin,
                  PermissionMappingMixin,
                  ModelViewSet):
    queryset = Site.objects.all()
    filterset_class = SiteFilter
    search_fields = ('name', 'locality')

    serializer_mapping = SerializerMapping.from_module(sites)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsCreator |
                IsAdmin
            )
        ],
    }, default=IsAuthenticated)

    def get_permissions(self):
        if self.action == Actions.CREATE:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == Actions.RETRIEVE:
            user = self.request.user
            site = self.get_object()

            if site.has_coordinate_permission(user):
                return sites.FullDetailSerializer
            return sites.DetailSerializer

        return super().get_serializer_class()
