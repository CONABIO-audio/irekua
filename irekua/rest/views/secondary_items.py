# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

from database import models as db
from rest.serializers import secondary_items
from .utils import CustomViewSet


class SecondaryItemViewSet(mixins.UpdateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           CustomViewSet):
    queryset = db.SecondaryItem.objects.all()
    serializer_module = secondary_items
