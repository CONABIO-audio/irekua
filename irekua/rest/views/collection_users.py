# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionUser
from rest.serializers import collection_users
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping


class CollectionUserViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            GenericViewSet):
    queryset = CollectionUser.objects.all()
    serializer_mapping = SerializerMapping.from_module(collection_users)
