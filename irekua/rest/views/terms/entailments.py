# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Entailment

from rest.serializers.terms import entailments

from rest.permissions import IsAdmin
from rest.permissions import IsCurator
from rest.permissions import ReadOnly

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class EntailmentViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        CustomViewSetMixin,
                        GenericViewSet):
    queryset = Entailment.objects.all()

    serializer_mapping = SerializerMapping.from_module(entailments)
    permission_mapping = PermissionMapping(
        default=IsAdmin | IsCurator | ReadOnly)
