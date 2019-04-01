# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models as db

from rest.serializers import secondary_items
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin


class SecondaryItemViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           SerializerMappingMixin,
                           GenericViewSet):
    queryset = db.SecondaryItem.objects.all()
    serializer_mapping = SerializerMapping.from_module(secondary_items)
