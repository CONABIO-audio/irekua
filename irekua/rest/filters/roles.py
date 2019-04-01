from database.models import Role
from .utils import BaseFilter


class RoleFilter(BaseFilter):
    class Meta:
        model = Role
        fields = (
            'name',
        )
