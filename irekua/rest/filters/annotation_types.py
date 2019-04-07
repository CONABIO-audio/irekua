from database.models import AnnotationType
from .utils import BaseFilter


search_fields = (
    'name',
)


class Filter(BaseFilter):
    class Meta:
        model = AnnotationType
        fields = ('name', )
