# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

import database.models as db
from rest.serializers import collection_users
from .utils import CustomViewSet


class CollectionUserViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSet):
    queryset = db.CollectionUser.objects.all()
    serializer_module = collection_users
