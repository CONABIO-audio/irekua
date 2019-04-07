from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated


class IsUnauthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super().has_permission(request, view)


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_developer


class IsModel(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_model


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_curator


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser


class IsSpecialUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser | user.is_curator | user.is_model | user.is_developer
