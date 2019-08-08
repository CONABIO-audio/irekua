from django import forms
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter

from database.models import Annotation


class Filter(FilterSet):
    created_on_from = DateFilter(field_name="created_on",lookup_expr='gt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    created_on_to = DateFilter(field_name="created_on",lookup_expr='lt',widget=forms.DateInput(attrs={'class': 'datepicker'}))
    class Meta:
        model = Annotation
        fields = {
            'annotation_type': ['exact'],
            'event_type': ['exact'],
            'created_by__username': ['exact', 'contains'],
            'certainty' : ['exact']
            }


search_fields = (
    'annotation_type',
    'event_type',
    'created_by__username',
    'created_on'
)

ordering_fields = (
    ('created_on', _('added on')),
    ('annotation_type', _('annotation type')),
    ('event_type', _('event type')),


)