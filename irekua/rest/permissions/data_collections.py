from rest_framework.permissions import BasePermission


class HasUpdatePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.has_permission(user, 'change_collection')


class IsCollectionAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.is_admin(user)


class IsCollectionTypeAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        collection_type = obj.collection_type
        return collection_type.is_admin(user)

class IsCollectionUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj.has_user(user)


class HasAddLicencePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return obj.has_permission(user, 'add_collection_licence')


class HasAddDevicePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return obj.has_permission(user, 'add_collection_device')


class HasAddSitePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return obj.has_permission(user, 'add_collection_site')


class HasAddUserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return obj.has_permission(user, 'add_collection_user')


class HasAddSamplingEventPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        user = request.user
        return obj.has_permission(user, 'add_collection_sampling_event')
