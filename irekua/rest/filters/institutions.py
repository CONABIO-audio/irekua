from database.models import Institution
from .utils import BaseFilter


class InstitutionFilter(BaseFilter):
    class Meta:
        model = Institution
        fields = (
            'institution_name',
            'institution_code',
            'subdependency',
            'country'
        )
