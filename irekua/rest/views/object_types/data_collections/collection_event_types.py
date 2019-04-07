# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import CollectionType

from rest.serializers.object_types.data_collections import collection_event_types

from rest.permissions import ReadOnly
from rest.permissions import IsAdmin

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class CollectionTypeEventTypeViewSet(mixins.RetrieveModelMixin,
                                     mixins.DestroyModelMixin,
                                     CustomViewSetMixin,
                                     GenericViewSet):
    queryset = CollectionType.event_types.through.objects.all()
    serializer_mapping = SerializerMapping.from_module(
        collection_event_types)

    permission_mapping = PermissionMapping(default=IsAdmin | ReadOnly)
