# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.permissions import IsAuthenticated
import django_filters

import database.models as db
from rest.serializers import sites
from rest.permissions import IsAdmin, ReadOnly
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    latitude__gt = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='gt')
    latitude__lt = django_filters.NumberFilter(
        field_name='latitude',
        lookup_expr='lt')

    longitude__gt = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='gt')
    longitude__lt = django_filters.NumberFilter(
        field_name='longitude',
        lookup_expr='lt')

    altitude__gt = django_filters.NumberFilter(
        field_name='altitude',
        lookup_expr='gt')
    altitude__lt = django_filters.NumberFilter(
        field_name='altitude',
        lookup_expr='lt')

    class Meta:
        model = db.Site
        fields = (
            'name',
            'site_type__name',
            'locality',
            'creator',
        )


class SiteViewSet(BaseViewSet):
    queryset = db.Site.objects.all()
    serializer_module = sites
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'locality')
    filterset_class = Filter

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
            else:
                return sites.DetailSerializer

        return super().get_serializer_class()


class CollectionSiteViewSet(BaseViewSet):
    queryset = db.Site.objects.all()
    serializer_module = sites
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'locality')
    filterset_class = Filter

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
            else:
                return sites.DetailSerializer

        return super().get_serializer_class()
