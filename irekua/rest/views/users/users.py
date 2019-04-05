# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import mixins

from database.models import Item
from database.models import User

from rest.serializers.users import users
from rest.serializers import items as item_serializers
from rest.serializers import sites as site_serializers
from rest.serializers.devices import physical_devices as device_serializers
from rest.serializers.sampling_events import sampling_events as sampling_event_serializers
from rest.serializers import SerializerMapping
from rest.serializers import SerializerMappingMixin
from rest.permissions import IsAdmin, ReadOnly, IsUser, IsUnauthenticated
from rest.filters import UserFilter

from rest.views.utils import AdditionalActionsMixin


class UserViewSet(mixins.UpdateModelMixin,
                  mixins.RetrieveModelMixin,
                  SerializerMappingMixin,
                  AdditionalActionsMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilter
    permission_classes = (IsAdmin | IsUser | ReadOnly, )

    serializer_mapping = (
        SerializerMapping
        .from_module(users)
        .extend(
            items=item_serializers.ListSerializer,
            devices=device_serializers.ListSerializer,
            sites=site_serializers.ListSerializer,
            sampling_events=sampling_event_serializers.ListSerializer,
        ))

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdmin | IsUnauthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            try:
                user = self.request.user
                viewed_user = self.get_object()

                if user == viewed_user or user.is_superuser:
                    return users.FullDetailSerializer
            except (AssertionError, AttributeError):
                return users.DetailSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=['GET'])
    def items(self, request, pk=None):
        user = self.get_object()
        queryset = Item.objects.filter(
            sampling_event__created_by=user)
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['GET'])
    def devices(self, request, pk=None):
        user = self.get_object()
        queryset = user.physicaldevice_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['GET'])
    def sites(self, request, pk=None):
        user = self.get_object()
        queryset = user.site_set.all()
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['GET'])
    def sampling_events(self, request, pk=None):
        user = self.get_object()
        queryset = user.sampling_event_created_by.all()
        return self.list_related_object_view(queryset)
