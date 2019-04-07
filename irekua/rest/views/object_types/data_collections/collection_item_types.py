# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionItemType

from rest.serializers.object_types.data_collections import collection_item_types

from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class CollectionTypeItemTypeViewSet(mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    CustomViewSetMixin,
                                    GenericViewSet):
    queryset = CollectionItemType.objects.all()
    serializer_mapping = SerializerMapping.from_module(
        collection_item_types)

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
