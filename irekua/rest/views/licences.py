# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Licence

from rest.serializers import licences

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import licences as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class LicenceViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     CustomViewSetMixin,
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
