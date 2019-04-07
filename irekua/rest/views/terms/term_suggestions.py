# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from database.models import TermSuggestion

from rest.serializers.terms import term_suggestions

from rest.permissions import IsAdmin
from rest.permissions import ReadOnly
from rest.permissions import term_suggestions as permissions

from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class TermSuggestionViewSet(mixins.UpdateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.DestroyModelMixin,
                            CustomViewSetMixin,
                            GenericViewSet):
    queryset = TermSuggestion.objects.all()

    serializer_mapping = SerializerMapping.from_module(term_suggestions)

    permission_mapping = PermissionMapping(
        default=permissions.IsOwnSuggestion | IsAdmin | ReadOnly)
