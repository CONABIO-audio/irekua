# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

from database import models as db
from rest.serializers import annotations
from .utils import CustomViewSet


class AnnotationViewSet(mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin,
                        CustomViewSet):
    queryset = db.Annotation.objects.all()
    serializer_module = annotations
