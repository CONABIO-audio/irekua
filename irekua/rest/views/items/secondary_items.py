# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SecondaryItem

from rest.serializers.items import secondary_items

from rest.permissions import IsAuthenticated

# from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class SecondaryItemViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           CustomViewSetMixin,
                           GenericViewSet):
    queryset = SecondaryItem.objects.all()

    permission_mapping = PermissionMapping(default=IsAuthenticated) # TODO: Fix permissions
    serializer_mapping = SerializerMapping.from_module(secondary_items)
