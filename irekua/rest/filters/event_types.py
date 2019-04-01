from database.models import EventType
from .utils import BaseFilter


class EventTypeFilter(BaseFilter):
    class Meta:
        model = EventType
        fields = ('name', )
