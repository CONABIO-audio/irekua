from database.models import MetaCollection
from .utils import BaseFilter


class MetaCollectionFilter(BaseFilter):
    class Meta:
        model = MetaCollection
        fields = (
            'name',
        )
