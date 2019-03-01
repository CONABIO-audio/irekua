# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import TermSuggestionSerializer


# Create your views here.
class TermSuggestionViewSet(viewsets.ModelViewSet):
    queryset = db.TermSuggestion.objects.all()
    serializer_class = TermSuggestionSerializer
