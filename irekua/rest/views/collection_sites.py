# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from database.models import CollectionSite

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest.serializers import sites
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping


class CollectionSiteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            GenericViewSet):
    queryset = CollectionSite.objects.all()
    serializer_mapping = SerializerMapping.from_module(sites)
