# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Institution

from rest.serializers.users import institutions

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
from rest.permissions import institutions as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class InstitutionViewSet(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         CustomViewSetMixin,
                         GenericViewSet):
    queryset = Institution.objects.all()

    serializer_mapping = SerializerMapping.from_module(institutions)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated,
            (
                permissions.IsFromInstitution |
                IsAdmin
            )
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin
        ],
    }, default=IsAuthenticated)
