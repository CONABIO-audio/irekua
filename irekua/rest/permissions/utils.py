from rest_framework.permissions import BasePermission


class Deny(BasePermission):
    def has_permission(self, request, view):
        return False


class PermissionMapping(object):
    DEFAULT_PERMISSION = [Deny]

    def __init__(self, mapping=None, default=None):
        if mapping is None:
            mapping = {}

        assert isinstance(mapping, dict)

        self.permission_mapping = mapping

        if default is None:
            default = PermissionMapping.DEFAULT_PERMISSION

        if not isinstance(default, (tuple, list)):
            default = [default]

        self.default_permission = default

    def get_permissions(self, action):
        try:
            permissions = self.permission_mapping[action]
            if not isinstance(permissions, (list, tuple)):
                return [permissions]
            return permissions
        except KeyError:
            return self.default_permission

    def extend(self, additional_actions=None, **kwargs):
        if additional_actions is None:
            additional_actions = {}

        extended_mapping = self.permission_mapping.copy()
        extended_mapping.update(additional_actions)

        for key in kwargs:
            extended_mapping[key] = kwargs[key]

        return PermissionMapping(extended_mapping)


class PermissionMappingMixin(object):
    @property
    def permission_mapping(self):
        raise NotImplementedError

    def get_permissions(self):
        permission_classes = self.permission_mapping.get_permissions(self.action)
        return [permission() for permission in permission_classes]
