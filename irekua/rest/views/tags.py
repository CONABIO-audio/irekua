# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

import database.models as db

from rest.serializers import tags
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import TagFilter


class TagViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = db.Tag.objects.all()
    serializer_mapping = SerializerMapping.from_module(tags)
    search_fields = ('name', )
    filterset_class = TagFilter
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
