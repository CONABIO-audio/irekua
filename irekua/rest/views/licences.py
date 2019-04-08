# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import licences as permissions


class LicenceViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     utils.CustomViewSetMixin,
                     GenericViewSet):
    queryset = models.Licence.objects.all()  # pylint: disable=E1101

    serializer_mapping = utils.SerializerMapping.from_module(serializers.licences)

    permission_mapping = utils.PermissionMapping({
        utils.Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsSigner |
                IsAdmin
            )
        ],
        utils.Actions.RETRIEVE: IsAuthenticated,
        utils.Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsSigner |
                IsAdmin
            )
        ],
    })
