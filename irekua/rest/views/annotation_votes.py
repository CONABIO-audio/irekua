# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from database.models import AnnotationVote

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from rest.serializers import annotation_votes
from rest.serializers import SerializerMappingMixin
from rest.serializers import SerializerMapping


class AnnotationVoteViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            SerializerMappingMixin,
                            GenericViewSet):
    queryset = AnnotationVote.objects.all()
    serializer_mapping = SerializerMapping.from_module(annotation_votes)
