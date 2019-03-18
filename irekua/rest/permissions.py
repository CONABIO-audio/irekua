from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    SAFE_METHODS
)


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


class IsCollectionUser(BasePermission):
    def has_permission(self, request, view):
        return True


class IsCollectionTypeCoordinator(BasePermission):
    def has_permission(self, request, view):
        return True


class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.userdata.is_developer
        except AttributeError:
            return False


class IsModel(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.userdata.is_model
        except AttributeError:
            return False


class IsCurator(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.userdata.is_curator
        except AttributeError:
            return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        try:
            return user.is_superuser | user.is_staff
        except AttributeError:
            return False


class IsFromInstitution(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        if user.is_superuser:
            return True

        if user.userdata is None:
            return False

        if user.userdata.institution is None:
            return False

        return user.userdata.institution == obj
