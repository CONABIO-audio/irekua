# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import Licence

from rest.serializers import licences
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin


class LicenceViewSet(mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     SerializerMappingMixin,
                     GenericViewSet):
    queryset = Licence.objects.all()
    serializer_mapping = SerializerMapping.from_module(licences)
