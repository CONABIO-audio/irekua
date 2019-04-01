# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import sites
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import SiteFilter


class SiteViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Site.objects.all()
    serializer_mapping = SerializerMapping.from_module(sites)
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'locality')
    filterset_class = SiteFilter

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            user = self.request.user
            site = self.get_object()

            if site.has_coordinate_permission(user):
                return sites.FullDetailSerializer
            return sites.DetailSerializer

        return super().get_serializer_class()
