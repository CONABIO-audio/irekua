# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import ModelViewSet

from database.models import Tag

from rest.serializers.items import tags
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadAndCreateOnly
from rest.filters import TagFilter


class TagViewSet(SerializerMappingMixin, ModelViewSet):
    queryset = Tag.objects.all()
    serializer_mapping = SerializerMapping.from_module(tags)
    search_fields = ('name', )
    filterset_class = TagFilter
    permission_classes = (IsAdmin | ReadAndCreateOnly, )
