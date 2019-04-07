# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import SynonymSuggestion

from rest.serializers.terms import synonym_suggestions

from rest.permissions import IsAuthenticated
from rest.permissions import IsAdmin
import rest.permissions.synonym_suggestions as permissions

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class SynonymSuggestionViewSet(mixins.UpdateModelMixin,
                               mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               CustomViewSetMixin,
                               GenericViewSet):

    queryset = SynonymSuggestion.objects.all()

    serializer_mapping = SerializerMapping.from_module(synonym_suggestions)
    permission_mapping = PermissionMapping({
        Actions.UPDATE: [
            IsAuthenticated, # TODO: Fix permissions
        ],
        Actions.DESTROY: [
            IsAuthenticated,
            IsAdmin
        ]
    }, default=IsAuthenticated)
