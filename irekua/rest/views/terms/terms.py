# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import ReadOnly


class TermViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  utils.CustomViewSetMixin,
                  GenericViewSet):
    queryset = models.Term.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.terms.terms)

    permission_mapping = utils.PermissionMapping(
        default=IsDeveloper | IsAdmin | ReadOnly)
