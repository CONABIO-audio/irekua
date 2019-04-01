from database.models import EntailmentType
from .utils import BaseFilter


class EntailmentTypeFilter(BaseFilter):
    class Meta:
        model = EntailmentType
        fields = (
            'source_type__name',
            'target_type__name',
        )
