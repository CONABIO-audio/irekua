from database.models import Tag
from .utils import BaseFilter

class TagFilter(BaseFilter):
    class Meta:
        model = Tag
        fields = (
            'name',
        )
