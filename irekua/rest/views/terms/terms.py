# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database.models import Term

from rest.serializers.terms import terms

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class TermViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  CustomViewSetMixin,
                  GenericViewSet):
    queryset = Term.objects.all()

    serializer_mapping = SerializerMapping.from_module(terms)

    permission_mapping = PermissionMapping(
        default=IsDeveloper | IsAdmin | ReadOnly)
