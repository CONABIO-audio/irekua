from rest_framework.permissions import BasePermission


class IsCollectionUser(BasePermission):
    def has_permission(self, request, view):
        return True

class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        pass
