from database.models import Collection
from .utils import BaseFilter


class CollectionFilter(BaseFilter):
    class Meta:
        model = Collection
        fields = (
            'name',
            'collection_type__name',
            'institution__institution_code',
            'institution__institution_name',
            'institution__country',
        )
