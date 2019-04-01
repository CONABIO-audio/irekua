from database.models import Synonym
from .utils import BaseFilter


class SynonymFilter(BaseFilter):
    class Meta:
        model = Synonym
        fields = (
            'source__term_type__name',
            'source__value',
            'target__term_type__name',
            'target__value'
        )
