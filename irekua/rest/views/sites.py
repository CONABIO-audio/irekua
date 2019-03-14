# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
import django_filters

import database.models as db
from rest.serializers.sites import SiteSerializer, FullSiteSerializer
from rest.permissions import IsAdmin, ReadOnly


class SiteFilter(django_filters.FilterSet):
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


class SiteViewSet(viewsets.ModelViewSet):
    queryset = db.Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (IsAdmin | ReadOnly, )
    search_fields = ('name', 'locality')
    filterset_class = SiteFilter

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def has_coordinate_permissions(self, user):
        return user.is_superuser

    def get_serializer_class(self):
        try:
            user = self.request.user
        except:
            return SiteSerializer

        if self.has_coordinate_permissions(user):
            return FullSiteSerializer
        else:
            return SiteSerializer
