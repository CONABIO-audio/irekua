from database.models import AnnotationType
from .utils import BaseFilter


class AnnotationTypeFilter(BaseFilter):
    class Meta:
        model = AnnotationType
        fields = ('name', )
