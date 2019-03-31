# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

import database.models as db
from rest.serializers import items
from .utils import CustomViewSet


class CollectionItemViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSet):
    serializer_module = items
