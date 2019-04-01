from database.models import Annotation
from .utils import BaseFilter


class AnnotationFilter(BaseFilter):
    class Meta:
        model = Annotation
        fields = (
            'annotation_type__name',
            'annotation_tool__name',
            'event_type__name',
            'annotation_type__name',
            'quality',
            'created_by__username',
            'modified_by__username',
        )
