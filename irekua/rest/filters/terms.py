from database.models import Term
from .utils import BaseFilter


class TermFilter(BaseFilter):
    class Meta:
        model = Term
        fields = (
            'term_type__name',
            'value'
        )
