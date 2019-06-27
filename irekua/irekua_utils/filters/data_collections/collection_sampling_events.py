from django.utils.translation import gettext as _
from django_filters import FilterSet

from database.models import SamplingEvent


class Filter(FilterSet):
    class Meta:
        model = SamplingEvent
        fields = [
            'created_on',
            'created_by',
            'sampling_event_type',
            'collection_site__site__name',
            'started_on',
            'ended_on'
        ]


search_fields = (
    'internal_id',
    'created_on',
    'created_by',
    'sampling_event_type',
    'collection_site__site__name',
    'started_on',
    'ended_on'
)


ordering_fields = (
    ('created_on', _('added on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
    ('internal_id', _('internal id'))
)