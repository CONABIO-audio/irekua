# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from database import models
from rest import serializers
from rest import utils

from rest.permissions import IsAdmin
from rest.permissions import IsDeveloper
from rest.permissions import IsAuthenticated


class EventTypeViewSet(mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.UpdateModelMixin,
                       utils.CustomViewSetMixin,
                       GenericViewSet):
    queryset = models.EventType.objects.all()  # pylint: disable=E1101

    permission_mapping = utils.PermissionMapping({
        utils.Actions.RETRIEVE: IsAuthenticated,
        utils.Actions.UPDATE: [
            IsAuthenticated,
            IsDeveloper | IsAdmin
        ],
    }, default=IsDeveloper | IsAdmin)

    serializer_mapping = (
        utils.SerializerMapping
        .from_module(serializers.object_types.events)
        .extend(
            add_term_types=serializers.object_types.terms.SelectSerializer,
            remove_term_types=serializers.object_types.terms.SelectSerializer,
        ))

    @action(detail=True, methods=['POST'])
    def add_term_types(self, request, pk=None):
        return self.add_related_object_view(models.TermType, 'term_type')

    @action(detail=True, methods=['POST'])
    def remove_term_types(self, request, pk=None):
        return self.remove_related_object_view('term_type')
