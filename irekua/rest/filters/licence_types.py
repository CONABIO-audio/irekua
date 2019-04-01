from database.models import LicenceType
from .utils import BaseFilter


class LicenceTypeFilter(BaseFilter):
    class Meta:
        model = LicenceType
        fields = (
            'name',
            'years_valid_for',
            'can_view',
            'can_download',
            'can_view_annotations',
            'can_annotate',
            'can_vote_annotations'
        )
