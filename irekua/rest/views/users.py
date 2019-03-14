# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets

from database.models import User
from rest.serializers.users import UserSerializer, FullUserSerializer
from rest.permissions import IsAdmin, ReadOnly, IsUser, IsUnauthenticated


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = (IsAdmin | IsUser | ReadOnly,)

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsUnauthenticated]
        else:
            permission_classes = self.permission_classes

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        try:
            user = self.request.user
            viewed_user = self.get_object()

            if user == viewed_user or user.is_superuser:
                return FullUserSerializer
        except:
            pass

        return UserSerializer
