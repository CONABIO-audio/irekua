from database.models import CollectionType
from .utils import BaseFilter


class CollectionTypeFilter(BaseFilter):
    class Meta:
        model = CollectionType
        fields = (
            'name',
            'anyone_can_create',
        )
