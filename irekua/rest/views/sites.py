# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from database.models import Site
from database.models import SiteType

from rest.serializers import sites
from rest.serializers.object_types import site_types
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
import rest.permissions.sites as permissions

from rest.filters import SiteFilter
from rest.utils import Actions
from rest.views.utils import AdditionalActionsMixin


class SiteViewSet(SerializerMappingMixin,
                  PermissionMappingMixin,
                  AdditionalActionsMixin,
                  ModelViewSet):
    queryset = Site.objects.all()
    filterset_class = SiteFilter
    search_fields = ('name', 'locality')

    serializer_mapping = (
        SerializerMapping
        .from_module(sites)
        .extend(
            types=site_types.ListSerializer,
            add_type=site_types.CreateSerializer,
        ))

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
        'add_type': [IsAuthenticated, IsAdmin]
    }, default=IsAuthenticated)

    def get_serializer_class(self):
        if self.action == Actions.RETRIEVE:
            user = self.request.user
            site = self.get_object()

            if site.has_coordinate_permission(user):
                return sites.FullDetailSerializer
            return sites.DetailSerializer

        return super().get_serializer_class()

    @action(detail=False, methods=['GET'])
    def types(self, request):
        queryset = SiteType.objects.all()
        return self.list_related_object_view(queryset)

    @types.mapping.post
    def add_type(self, request):
        self.create_related_object_view()
