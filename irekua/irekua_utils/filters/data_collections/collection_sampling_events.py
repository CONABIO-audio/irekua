from django import forms
from django.db import models
from django.utils.translation import gettext as _
from django_filters import FilterSet,DateFilter
from django_filters import BooleanFilter


from database.models import SamplingEvent


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())
    class Meta:
        model = SamplingEvent
        fields = {
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
            'sampling_event_type': ['exact'],
            'collection_site__site__name': ['icontains'],
            'started_on': ['gt', 'lt'],
            'ended_on': ['gt', 'lt'],
            'created_on': ['gt', 'lt'],
        }

        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            }
        }
    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(physical_device__created_by=user)
        return queryset

search_fields = (
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
    ('ended_on', _('ended on'))
)
