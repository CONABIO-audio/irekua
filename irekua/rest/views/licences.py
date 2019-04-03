# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Licence

from rest.serializers import licences
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin

from rest.permissions import PermissionMapping
from rest.permissions import PermissionMappingMixin
from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import licences as permissions

from rest.utils import Actions


class LicenceViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     SerializerMappingMixin,
                     PermissionMappingMixin,
                     GenericViewSet):
    queryset = Licence.objects.all()
    serializer_mapping = SerializerMapping.from_module(licences)

    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsSigner |
                IsAdmin
            )
        ],
        Actions.RETRIEVE: IsAuthenticated,
        Actions.DESTROY: [
            IsAuthenticated,
            (
                permissions.IsSigner |
                IsAdmin
            )
        ],
    })
