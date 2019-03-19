# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from database.models import User
from rest.serializers import users
from rest.permissions import IsAdmin, ReadOnly, IsUser, IsUnauthenticated
from rest.filters import BaseFilter
from .utils import BaseViewSet


class Filter(BaseFilter):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'userdata__institution__institution_name',
            'userdata__institution__institution_code',
            'userdata__institution__subdependency',
        )


class UserViewSet(BaseViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_module = users
    filterset_class = Filter
    search_fields = (
        'username',
        'first_name',
        'last_name',
    )
    permission_classes = (IsAdmin | IsUser | ReadOnly, )

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
            except:
                return users.DetailSerializer

        if self.action in ['update', 'partial_update']:
            return users.UpdateSerializer

        return super().get_serializer_class()
