# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import utils
from rest import serializers


class CollectionTypeItemTypeViewSet(mixins.RetrieveModelMixin,
                                    mixins.DestroyModelMixin,
                                    utils.CustomViewSetMixin,
                                    GenericViewSet):
    queryset = models.CollectionItemType.objects.all()  # pylint: disable=E1101
    
    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.object_types.data_collections.items)

    permission_mapping = utils.PermissionMapping()
