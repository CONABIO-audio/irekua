from database.models import ItemType
from .utils import BaseFilter


class ItemTypeFilter(BaseFilter):
    class Meta:
        model = ItemType
        fields = (
            'name',
            'media_type'
        )
