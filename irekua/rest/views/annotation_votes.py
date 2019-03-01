# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import AnnotationVoteSerializer


# Create your views here.
class AnnotationVoteViewSet(viewsets.ModelViewSet):
    queryset = db.AnnotationVote.objects.all()
    serializer_class = AnnotationVoteSerializer
