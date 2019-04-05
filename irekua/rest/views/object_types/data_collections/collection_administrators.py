# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionType

from rest.serializers.object_types.data_collections import collection_administrators
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin

from rest.utils import Actions


class CollectionTypeAdministratorViewSet(mixins.RetrieveModelMixin,
                                         mixins.DestroyModelMixin,
                                         SerializerMappingMixin,
                                         PermissionMappingMixin,
                                         GenericViewSet):
    queryset = CollectionType.administrators.through.objects.all()
    serializer_mapping = SerializerMapping.from_module(collection_administrators)

    permission_mapping = PermissionMapping({
        Actions.RETRIEVE: IsAuthenticated,
    }, default=[IsAuthenticated, IsAdmin])
