# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import institutions as permissions


class InstitutionViewSet(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         utils.CustomViewSetMixin,
                         GenericViewSet):
    queryset = models.Institution.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(
        serializers.users.institutions)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsFromInstitution |
                IsAdmin
            )
        ],
        utils.Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin
        ],
    }, default=IsAuthenticated)
