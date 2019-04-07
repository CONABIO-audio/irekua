# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework import mixins

from database.models import Item
from database.models import PhysicalDevice
from database.models import Site
from database.models import User
from database.models import Role
from database.models import Institution

from rest.serializers.users import users
from rest.serializers.users import institutions as institution_serializers
from rest.serializers.users import roles as role_serializers
from rest.serializers.items  import items as item_serializers
from rest.serializers import sites as site_serializers
from rest.serializers.devices import physical_devices as device_serializers

from rest.permissions import IsAdmin
from rest.permissions import IsAuthenticated
from rest.permissions import IsUnauthenticated
from rest.permissions import users as permissions

from rest.filters import UserFilter
from rest.filters import RoleFilter
from rest.filters import ItemFilter
from rest.filters import PhysicalDeviceFilter
from rest.filters import SiteFilter
from rest.filters import InstitutionFilter

from rest.utils import Actions
from rest.utils import CustomViewSetMixin
from rest.utils import SerializerMapping
from rest.utils import PermissionMapping


class UserViewSet(mixins.ListModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  CustomViewSetMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    filterset_class = UserFilter

    permission_mapping = PermissionMapping({
        Actions.CREATE: IsUnauthenticated,
        Actions.UPDATE: [
            IsAuthenticated,
            permissions.IsSelf | IsAdmin
        ], # TODO: Fix permissions 
    }, default=IsAuthenticated)

    serializer_mapping = (
        SerializerMapping
        .from_module(users)
        .extend(
            items=item_serializers.ListSerializer,
            devices=device_serializers.ListSerializer,
            sites=site_serializers.ListSerializer,
            roles=role_serializers.ListSerializer,
            add_role=role_serializers.CreateSerializer,
            institutions=institution_serializers.ListSerializer,
            add_institution=institution_serializers.CreateSerializer,
        ))

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

    def get_queryset(self):
        if self.action == 'roles':
            return Role.objects.all()

        if self.action == 'institutions':
            return Institution.objects.all()

        if self.action == 'items':
            user_id = self.kwargs['pk']
            return Item.objects.filter(created_by=user_id)

        if self.action == 'devices':
            user_id = self.kwargs['pk']
            return PhysicalDevice.objects.filter(owner=user_id)

        if self.action == 'sites':
            user_id = self.kwargs['pk']
            return Site.objects.filter(created_by=user_id)

        return super().get_queryset()

    @action(detail=False, methods=['GET'], filterset_class=RoleFilter)
    def roles(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @roles.mapping.post
    def add_role(self, request):
        return self.create_related_object_view()

    @action(detail=False, methods=['GET'], filterset_class=InstitutionFilter)
    def institutions(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @institutions.mapping.post
    def add_institution(self, request):
        return self.create_related_object_view()

    @action(detail=True, methods=['GET'], filterset_class=ItemFilter)
    def items(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['GET'], filterset_class=PhysicalDeviceFilter)
    def devices(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)

    @action(detail=True, methods=['GET'], filterset_class=SiteFilter)
    def sites(self, request, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        return self.list_related_object_view(queryset)
