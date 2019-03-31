# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins

from rest.serializers import annotation_votes
from .utils import CustomViewSet


class AnnotationVoteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSet):
    serializer_module = annotation_votes
