from database.models import Entailment
from .utils import BaseFilter


class EntailmentFilter(BaseFilter):
    class Meta:
        model = Entailment
        fields = (
            'source__value',
            'source__term_type__name',
            'target__value',
            'target__term_type__name',
        )
