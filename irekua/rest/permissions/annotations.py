from rest_framework.permissions import IsAuthenticated


class CanUpdate(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True


class CanRetrieve(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True


class CanDestroy(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True


class CanList(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True


class CanListVotes(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True


class CanVote(IsAuthenticated):
    def has_permission(self, request, view):
        user = request.user
        return True
