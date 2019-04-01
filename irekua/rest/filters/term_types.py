from database.models import TermType
from .utils import BaseFilter


class TermTypeFilter(BaseFilter):
    class Meta:
        model = TermType
        fields = ('name', )
