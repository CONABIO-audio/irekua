# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

import database.models as db
from rest.serializers import sites
from .utils import CustomViewSet


class CollectionSiteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSet):
    queryset = db.Site.objects.all()
    serializer_module = sites
