# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SiteTypeSerializer
from rest.permissions import IsAdmin, ReadOnly

class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = db.Site
        fields = (
            'url',
            'name',
            'locality',
            'site_type',
            'geo_ref',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
            'creator'
        )


class SiteTypeViewSet(viewsets.ModelViewSet):
    queryset = db.SiteType.objects.all()
    serializer_class = SiteTypeSerializer
    permission_classes = (IsAdmin|ReadOnly, )
    search_fields = ('name', )
    filter_fields = ('name', )

    @action(detail=True, methods=['GET'])
    def sites(self, request, pk=None):
        try:
            site_type = db.SiteType.objects.get(pk=pk)
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        sites = site_type.site_set.all()
        page = self.paginate_queryset(sites)

        if page is not None:
            serializer = SiteSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = SiteSerializer(label_types, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], serializer_class=SiteSerializer)
    def create_site(self, request, pk=None):
        pass
