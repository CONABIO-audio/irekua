from database.models import User
from .utils import BaseFilter


class UserFilter(BaseFilter):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'institution__institution_name',
            'institution__institution_code',
            'institution__subdependency',
            'is_superuser',
            'is_curator',
            'is_model',
            'is_developer',
        )
