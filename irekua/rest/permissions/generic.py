from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import SAFE_METHODS


class ReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super(ReadOnly, self).has_permission(request, view)
        if not is_auth:
            return False
        return request.method in SAFE_METHODS


class ReadAndCreateOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super(ReadAndCreateOnly, self).has_permission(request, view)
        if not is_auth:
            return False
        return request.method in list(SAFE_METHODS) + ['POST']


class ListAndCreateOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super(ListAndCreateOnly, self).has_permission(request, view)
        if not is_auth:
            return False
        if request.method == 'POST':
            return True
        return view.action == 'list'


class CreateOnly(IsAuthenticated):
    def has_permission(self, request, view):
        is_auth = super(CreateOnly, self).has_permission(request, view)
        if not is_auth:
            return False
        return request.method == 'POST'


class IsUser(BasePermission):
    def has_permission(self, request, view):
        try:
            viewed_user = view.get_object()
            user = request.user
            return viewed_user == user
        except:
            return False

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        try:
            viewed_object = view.get_object()
            user = request.user
            return viewed_object.owner == user
        except:
            return False


class IsUnauthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super(IsUnauthenticated, self).has_permission(request, view)


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
