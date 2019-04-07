from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = self.request.user
        return user == obj
