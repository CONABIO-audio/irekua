from django import forms
from django.db import models
from django.utils.translation import gettext as _

from django_filters import FilterSet
from django_filters import DateFilter
from django_filters import ModelChoiceFilter
from django_filters import BooleanFilter


from dal import autocomplete

from database.models import SamplingEvent


def get_url(f):
    try:
        return f.target_field.model.autocomplete_url
    except:
        return ''


def get_queryset(f):
    return f.target_field.model.objects.all()


class Filter(FilterSet):
    is_own = BooleanFilter(
        method='user_owns_object',
        label=_('Mine'),
        widget=forms.CheckboxInput())

    class Meta:
        model = SamplingEvent
        fields = {
            'sampling_event_type': ['exact'],
            'collection': ['exact'],
            'created_on': ['lt', 'gt'],
            'ended_on': ['lt', 'gt'],
            'started_on': ['lt', 'gt'],
            'collection_site': ['exact'],
            'collection_site__site__name': ['icontains'],
            'created_by': ['exact'],
            'created_by__username': ['icontains'],
            'created_by__first_name': ['icontains'],
            'created_by__last_name': ['icontains'],
        }


        filter_overrides = {
            models.DateTimeField: {
                'filter_class': DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'class': 'datepicker'})
                }
            },
            models.ForeignKey: {
                'filter_class': ModelChoiceFilter,
                'extra': lambda f: {
                    'queryset': get_queryset(f),
                    'widget': autocomplete.ModelSelect2(
                        url=get_url(f)
                    )
                }
            }
        }

    def user_owns_object(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(created_by=user)
        return queryset


search_fields = (
    'sampling_event_type__name',
    'collection_site__site__name',
    'collection__name',
)


ordering_fields = (
    ('created_on', _('added on')),
    ('started_on', _('started on')),
    ('ended_on', _('ended on')),
)
