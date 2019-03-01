# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets
import database.models as db

from rest.serializers import SynonymSuggestionSerializer


# Create your views here.
class SynonymSuggestionViewSet(viewsets.ModelViewSet):
    queryset = db.SynonymSuggestion.objects.all()
    serializer_class = SynonymSuggestionSerializer
