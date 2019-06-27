from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import SamplingEvent


class Filter(FilterSet):
    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact'],
            'started_on': ['gt', 'lt'],
            'ended_on': ['gt', 'lt'],
            'created_on': ['gt', 'lt'],
        }

search_fields = (
    'sampling_event_type',
    'collection',
)


ordering_fields = (
    ('created_on', _('created on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
)
