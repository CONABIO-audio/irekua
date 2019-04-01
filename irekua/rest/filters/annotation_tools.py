from database.models import AnnotationTool
from .utils import BaseFilter


class AnnotationToolFilter(BaseFilter):
    class Meta:
        model = AnnotationTool
        fields = (
            'name',
            'version')
