# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

import database.models as db

from rest.serializers import SiteTypeSerializer
from rest.permissions import IsAdmin, ReadOnly


class SiteSerializer(serializers.ModelSerializer):
    site_type_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:sitetype-detail',
        source='site_type')
    creator_url = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rest-api:user-detail',
        source='creator')
    creator = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username')

    class Meta:
        model = db.Site
        fields = (
            'url',
            'id',
            'name',
            'locality',
            'site_type',
            'site_type_url',
            'geo_ref',
            'latitude',
            'longitude',
            'altitude',
            'metadata',
            'creator',
            'creator_url',
        )
        extra_kwargs = {
            'creator': {'read_only': True},
            'site_type': {'read_only': True},
        }

    def create(self, validated_data):
        creator = self.context['request'].user
        site_type = self.context['site_type']

        validated_data['creator'] = creator
        validated_data['site_type'] = site_type

        return db.Site.objects.create(**validated_data)


class SiteTypeViewSet(viewsets.ModelViewSet):
    queryset = db.SiteType.objects.all()
    serializer_class = SiteTypeSerializer
    permission_classes = (IsAdmin | ReadOnly, )
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
            serializer = SiteSerializer(
                page,
                many=True,
                context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = SiteSerializer(sites, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'], serializer_class=SiteSerializer)
    def create_site(self, request, pk=None):
        try:
            site_type = db.SiteType.objects.get(pk=pk)
        except db.EventType.DoesNotExist as error:
            return Response(str(error), status=status.HTTP_404_NOT_FOUND)

        serializer = SiteSerializer(
            data=request.data,
            context={'request': request, 'site_type': site_type})

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)

        else:
            site = serializer.save()

        site_type.site_set.add(site)
        site_type.save()

        return Response(status=status.HTTP_201_CREATED)
